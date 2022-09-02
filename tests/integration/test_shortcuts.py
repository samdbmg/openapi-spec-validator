import pytest

from openapi_spec_validator import openapi_v2_spec_validator
from openapi_spec_validator import openapi_v30_spec_validator
from openapi_spec_validator import validate_spec
from openapi_spec_validator import validate_spec_factory
from openapi_spec_validator import validate_spec_url
from openapi_spec_validator import validate_spec_url_factory
from openapi_spec_validator import validate_v2_spec
from openapi_spec_validator import validate_v2_spec_url
from openapi_spec_validator import validate_v30_spec
from openapi_spec_validator import validate_v30_spec_url
from openapi_spec_validator.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


class TestValidateSpec:
    def test_spec_schema_version_not_detected(self):
        spec = {}

        with pytest.raises(ValidatorDetectError):
            validate_spec(spec)


class TestValidateSpecUrl:
    def test_spec_schema_version_not_detected(self, factory):
        spec_path = "data/empty.yaml"
        spec_url = factory.spec_file_url(spec_path)

        with pytest.raises(ValidatorDetectError):
            validate_spec_url(spec_url)


class TestValidatev2Spec:

    LOCAL_SOURCE_DIRECTORY = "data/v2.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        validate_spec(spec)
        validate_v2_spec(spec)

        validate_spec_factory(openapi_v2_spec_validator)(spec, spec_url)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_falied(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)

        with pytest.raises(OpenAPIValidationError):
            validate_v2_spec(spec)


class TestValidatev30Spec:

    LOCAL_SOURCE_DIRECTORY = "data/v3.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        validate_spec(spec)
        validate_v30_spec(spec)

        validate_spec_factory(openapi_v30_spec_validator)(spec, spec_url)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_falied(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)

        with pytest.raises(OpenAPIValidationError):
            validate_v30_spec(spec)


class TestValidatev2SpecUrl:

    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/petstore.yaml",
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/api-with-examples.yaml",
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/petstore-expanded.yaml",
        ],
    )
    def test_valid(self, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)

        validate_spec_url(spec_url)
        validate_v2_spec_url(spec_url)

        validate_spec_url_factory(openapi_v2_spec_validator)(spec_url)


class TestValidatev30SpecUrl:

    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "petstore.yaml",
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "api-with-examples.yaml",
            "970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/"
            "api-with-examples.yaml",
        ],
    )
    def test_valid(self, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)

        validate_spec_url(spec_url)
        validate_v30_spec_url(spec_url)

        validate_spec_url_factory(openapi_v30_spec_validator)(spec_url)
