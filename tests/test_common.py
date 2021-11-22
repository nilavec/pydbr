import base64
import pytest
import pydbr

def test_link_property_bearer_token_returns_correct_value(dbc, pydbr_fix):
    assert dbc.link.bearer_token == pydbr_fix.dastabricks_token

def test_link_property_url_returns_correct_value(dbc, pydbr_fix):
    assert dbc.link.url == pydbr_fix.databricks_url

def test_link_property_cluster_id_correct_value(dbc, pydbr_fix):
    assert dbc.link.cluster_id == pydbr_fix.databricks_cluster_id


def test_link_get_returns_parsed_response(dbc):
    response = dbc.link.get(verb='dbfs/list', params={'path':'/'})
    assert isinstance(response, dict)
    assert 'files' in response

def test_link_get_with_bad_params_raises_exception(dbc):
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        response = dbc.link.get(verb='dbfs/list')
    assert excinfo.value.error_code == 'INVALID_PARAMETER_VALUE'


def test_link_post_with_json_returns_parsed_response(dbc, pydbr_fix):
    response = dbc.link.post(verb='dbfs/put', json={'path':f'{pydbr_fix.dbfs_tmp}/test_link_put.txt',
                                                     'contents': base64.b64encode(b'Hello, pydbr!').decode(), 
                                                     'overwrite': True,
                                                    },
                             params={})
    assert isinstance(response, dict)
    assert {} == response


def test_link_put_with_basd_params_raises_exception(dbc, pydbr_fix):
    
    # Missing contents parameter
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        response = dbc.link.post(verb='dbfs/put', json={'path':f'{pydbr_fix.dbfs_tmp}/test_link_put.txt',
                                                        #  'contents': base64.b64encode(b'Hello, pydbr!').decode(), 
                                                        'overwrite': True})
    
    assert excinfo.value.error_code == 'INVALID_PARAMETER_VALUE'


def test_api_has_property_link(dbc):
    api = pydbr.common.Api(dbc.link, 'dbfs')
    assert hasattr(api, 'link')
    assert isinstance(api.link, pydbr.common.Link)

def test_api_path_returns_path_to_action(dbc):
    api = pydbr.common.Api(dbc.link, 'dbfs')
    actual = api.path('list')
    assert 'dbfs/list' == actual


def test_bite_size_str_with_default_format():
    actual = pydbr.common.bite_size_str(100)
    assert '100 B' == actual
    actual = pydbr.common.bite_size_str(2500)
    assert '2.5 KB' == actual

def test_bite_size_str_with_custom_format():
    fmt = '{0:.3n} {1}pix'
    actual = pydbr.common.bite_size_str(200, fmt)
    assert '200 pix' == actual
    actual = pydbr.common.bite_size_str(3500, fmt)
    assert '3.5 Kpix' == actual



def test_DataClass():
    c = pydbr.databricks_data_classes.DataClass.from_dict({})

    d = c.asdict()
    assert isinstance(d, dict)

    for attr in c: # Can be iterated
        pass

