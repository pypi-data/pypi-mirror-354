from abc import ABC, abstractmethod
from orionis.test.suite.test_unit import UnitTest

class ITestSuite(ABC):

    @abstractmethod
    def run(self) -> UnitTest:
        """
        Runs the test suite based on the provided configuration.

        Initializes a UnitTest suite, configures it with parameters from the Configuration object,
        discovers test folders matching the specified pattern, adds the discovered tests to the suite,
        executes the test suite, and returns the results.

        Returns
        -------
        UnitTest
            The result of the executed test suite.

        Raises
        ------
        OrionisTestConfigException
            If the provided configuration is not an instance of Configuration.
        """
        pass