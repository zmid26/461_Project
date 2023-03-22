import connexion
import six

from swagger_server.models.authentication_request import AuthenticationRequest  # noqa: E501
from swagger_server.models.authentication_token import AuthenticationToken  # noqa: E501
from swagger_server.models.enumerate_offset import EnumerateOffset  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.package import Package  # noqa: E501
from swagger_server.models.package_data import PackageData  # noqa: E501
from swagger_server.models.package_history_entry import PackageHistoryEntry  # noqa: E501
from swagger_server.models.package_id import PackageID  # noqa: E501
from swagger_server.models.package_metadata import PackageMetadata  # noqa: E501
from swagger_server.models.package_name import PackageName  # noqa: E501
from swagger_server.models.package_query import PackageQuery  # noqa: E501
from swagger_server.models.package_rating import PackageRating  # noqa: E501
from swagger_server.models.package_reg_ex import PackageRegEx  # noqa: E501
from swagger_server import util


def create_auth_token(body):  # noqa: E501
    """create_auth_token

    Create an access token. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: AuthenticationToken
    """
    if connexion.request.is_json:
        body = AuthenticationRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_by_name_delete(name, x_authorization=None):  # noqa: E501
    """Delete all versions of this package.

     # noqa: E501

    :param name: 
    :type name: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        name = PackageName.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_by_name_get(name, x_authorization=None):  # noqa: E501
    """package_by_name_get

    Return the history of this package (all versions). # noqa: E501

    :param name: 
    :type name: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: List[PackageHistoryEntry]
    """
    if connexion.request.is_json:
        name = PackageName.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_by_reg_ex_get(body, regex, x_authorization=None):  # noqa: E501
    """Get any packages fitting the regular expression.

    Search for a package using regular expression over package names and READMEs. This is similar to search by name. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param regex: 
    :type regex: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: List[PackageMetadata]
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        regex = PackageRegEx.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_create(body, x_authorization):  # noqa: E501
    """package_create

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: Package
    """
    if connexion.request.is_json:
        body = PackageData.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_delete(id, x_authorization=None):  # noqa: E501
    """Delete this version of the package.

     # noqa: E501

    :param id: Package ID
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_rate(id, x_authorization=None):  # noqa: E501
    """package_rate

     # noqa: E501

    :param id: 
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: PackageRating
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_retrieve(id, x_authorization=None):  # noqa: E501
    """Interact with the package with this ID

    Return this package. # noqa: E501

    :param id: ID of package to fetch
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: Package
    """
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def package_update(body, id, x_authorization=None):  # noqa: E501
    """Update this content of the package.

    The name, version, and ID must match.  The package contents (from PackageData) will replace the previous contents. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: dict | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Package.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        id = PackageID.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def packages_list(body, x_authorization=None, offset=None):  # noqa: E501
    """Get the packages from the registry.

    Get any packages fitting the query. Search for packages satisfying the indicated query.  If you want to enumerate all packages, provide an array with a single PackageQuery whose name is \&quot;*\&quot;.  The response is paginated; the response header includes the offset to use in the next query. # noqa: E501

    :param body: 
    :type body: list | bytes
    :param x_authorization: 
    :type x_authorization: dict | bytes
    :param offset: Provide this for pagination. If not provided, returns the first page of results.
    :type offset: dict | bytes

    :rtype: List[PackageMetadata]
    """
    if connexion.request.is_json:
        body = [PackageQuery.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        offset = EnumerateOffset.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def registry_reset(x_authorization=None):  # noqa: E501
    """Reset the registry

    Reset the registry to a system default state. # noqa: E501

    :param x_authorization: 
    :type x_authorization: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        x_authorization = AuthenticationToken.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
