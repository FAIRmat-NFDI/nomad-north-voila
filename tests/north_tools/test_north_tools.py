def test_importing_north_tool():
    # this will raise an exception if pydantic model validation fails for the north tool
    from nomad_north_voila.north_tools import voila

    assert voila.id_url_safe == 'north_tool_voila' or voila.id == 'nomad-north-voila', (
        'NORTHTool entry point has incorrect id or id_url_safe'
    )
