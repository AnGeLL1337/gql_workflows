import pytest
from unittest.mock import patch
from GraphTypeDefinitions._GraphResolvers import resolve_user


@pytest.mark.asyncio
async def test_resolve_user_exception_handling():
    user_id = "16c92914-0f71-437d-ace3-9661abe4c6cd"
    # Mock the resolve_reference method to raise an Exception
    with patch('GraphTypeDefinitions.externals.UserGQLModel.resolve_reference',
               side_effect=Exception("Test Exception")) as mock_resolve_reference:
        result = await resolve_user(user_id)
        # Assert that the mock was called once with the correct parameters
        mock_resolve_reference.assert_called_once_with(id=user_id, info=None)
        # Assert that result is None due to exception handling
        assert result is None
