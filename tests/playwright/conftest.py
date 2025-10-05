import pytest


@pytest.fixture(scope="function", autouse=True)
def trace_on_failure(context, request):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    if request.node.rep_call.failed:
        trace_path = f"trace_{request.node.name}.zip"
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()
