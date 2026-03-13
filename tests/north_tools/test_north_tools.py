def test_importing_north_tool():
    # this will raise an exception if pydantic model validation fails for the north tool
    from nomad_north_voila.north_tools import voila_entry_point

    assert (
        voila_entry_point.id_url_safe == 'voila'
        or voila_entry_point.id == 'nomad-north-voila'
    ), 'NORTHTool entry point has incorrect id or id_url_safe'
