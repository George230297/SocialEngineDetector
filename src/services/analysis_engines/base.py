from abc import ABC, abstractmethod
from src.domain.schemas import ArtifactType, ScanRequest, ScanResult

class AnalysisEngine(ABC):
    """
    Abstract Base Class for all analysis engines (Strategy Pattern).
    """

    @abstractmethod
    def supports(self, artifact_type: ArtifactType) -> bool:
        """
        Determines if this engine supports the given artifact type.
        """
        pass

    @abstractmethod
    async def scan(self, request: ScanRequest) -> ScanResult:
        """
        Performs the analysis on the given request.
        This must be implemented as an asynchronous method.
        """
        pass
