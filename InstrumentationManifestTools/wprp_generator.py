import InstrumentationManifestTools.simple_xml as xml

def to_wprp_xml(profiles):

    wprp = xml.Node("WindowsPerformanceRecorder")
    wprp.attrs(Author = "N/A",
        Comments = "Auto generated",
        Copyright = "",
        Version = "1.0",
        Tag = "Enables providers"
    )

    for profile in profiles:
        description = profile.gui_name
        buffer_size = 64
        buffers = 64

        profiles_xml = wprp.add("Profiles")
        ec = profiles_xml.add("EventCollector",
            Id = profile.name,
            Name = "Sample Event Collector"
        )

        ec.add("BufferSize", Value = buffer_size)
        ec.add("Buffers", Value = buffers)

    detail_levels = [ "Verbose", "Light" ]
    logging_types = [ "Memory", "File" ]

    for profile in profiles:
        for detail_level in detail_levels:
            for logging_type in logging_types:
                collector_name = profile.name + "_Profile"

                p = profiles_xml.add("Profile",
                    Id = "{}.{}.{}".format(collector_name, detail_level, logging_type),
                    Name = collector_name,
                    Description = description,
                    DetailLevel = detail_level,
                    LoggingMode = logging_type
                )

                c = p.add("Collectors")
                eci = c.add("EventCollectorId", Value = profile.name)

                providers_xml = eci.add("EventProviders")
                for p, opts in profile.providers:
                    if opts.get(logging_type.lower(), True) == False:
                        continue

                    if opts.get(detail_level.lower(), True) == False:
                        continue

                    provider_xml = providers_xml.add("EventProvider",
                        Id = p.name + "_Provider",
                        Name = p.name
                    )
    return wprp.to_xml_document()
