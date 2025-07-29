import logging

from prophecy.utils.json_rpc_layer import *
from prophecy.utils.secrets import SecretCrudRequest, handle_secrets_crud

_HANDLER_REGISTRY: MappingProxyType[
    type[RequestMethod], Callable[[Any], Awaitable[JsonRpcResult]]
] = MappingProxyType(
    {
        DatasetRunsRequest: handle_dataset_runs,
        SecretCrudRequest: handle_secrets_crud
        # add more: AnotherRequest: handle_another,
    }
)

# ----- 2.2  async dispatcher (runs inside a background event‑loop) ---------
async def dispatch_em_request_async(
        req_msg: RequestMessage,
) -> ResponseMessage:  # noqa: D401
    req = req_msg.method

    if isinstance(req, EMRequest):
        await refresh_tables(req.filters)

    handler = _HANDLER_REGISTRY.get(type(req))
    if handler is None:
        raise RuntimeError(f"No handler registered for {type(req).__name__}")
    try:
        result = await handler(req)  # type: ignore[arg-type]
        return ResponseMessage.Success(id=req_msg.id, result=result)  # type: ignore[return-value]
    except Exception as exc:  # noqa: BLE001
        err = JsonRpcError(message=str(exc), trace=traceback.format_exc().splitlines())
        return ResponseMessage.Error(id=req_msg.id, error=err)  # type: ignore[return-value]

# ----- 2.3  background asyncio loop in daemon thread -----------------------
_EVENT_LOOP = asyncio.new_event_loop()
_thread = threading.Thread(target=_EVENT_LOOP.run_forever, daemon=True)
_thread.start()


def _schedule(coro: Awaitable[Any]):  # noqa: D401
    """Run *coro* in the background loop and return its result (blocking)."""
    return asyncio.run_coroutine_threadsafe(coro, _EVENT_LOOP).result()


###############################################################################
# 3.  WEBSOCKET‑CLIENT GLUE                                                 #
###############################################################################


def _process_request(
        payload_raw: str, ws
) -> None:  # noqa: D401
    """Handle one frame coming from Scala, send back a response frame."""

    try:
        payload_str = (
            json.dumps(payload_raw) if isinstance(payload_raw, dict) else payload_raw
        )
        req_msg = RequestMessage.from_json(payload_str)

        resp_msg = _schedule(dispatch_em_request_async(req_msg))
        logging.info(f'Sending back success response : {resp_msg}')
        from websocket_runner import send_message_via_ws
        send_message_via_ws(resp_msg.to_json())
    except Exception as exc:  # catch‑all: malformed frame
        err_resp = ResponseMessage.Error(
            id=str(uuid4()),
            error=JsonRpcError(
                message=str(exc), trace=traceback.format_exc().splitlines()
            ),
        )
        from websocket_runner import send_message_via_ws
        send_message_via_ws(err_resp.to_json())