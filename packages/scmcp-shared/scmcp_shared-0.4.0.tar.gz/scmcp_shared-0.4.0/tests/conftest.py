
import pytest
from scmcp_shared.server import BaseMCPManager
from scmcp_shared.server import ScanpyIOMCP
from scmcp_shared.server import ScanpyPreprocessingMCP
from scmcp_shared.server import ScanpyToolsMCP
from scmcp_shared.server import ScanpyPlottingMCP
from scmcp_shared.server import ScanpyUtilMCP


class ScanpyMCPManager(BaseMCPManager):
    """Manager class for Scanpy MCP modules."""
    
    def _init_modules(self):
        """Initialize available Scanpy MCP modules."""
        self.available_modules = {
            "io": ScanpyIOMCP().mcp,
            "pp": ScanpyPreprocessingMCP().mcp,
            "tl": ScanpyToolsMCP().mcp,
            "pl": ScanpyPlottingMCP().mcp,
            "ul": ScanpyUtilMCP().mcp
        }


@pytest.fixture
def mcp():
    return ScanpyMCPManager("scmcp").mcp




