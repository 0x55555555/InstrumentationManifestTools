import InstrumentationManifestTools.manifest as manifest
import InstrumentationManifestTools.wprp_generator
import InstrumentationManifestTools.manifest_generator

def sample():
    p = manifest.Provider("Multi-Main")

    task = manifest.Task("task1")
    p.add(task)

    op = manifest.Opcode("opcode")
    p.add(op)

    kw = manifest.Keyword("kw")
    p.add(kw)

    filter = manifest.Filter("fil")
    p.add(filter)

    lev = manifest.Level("lev")
    p.add(lev)

    templ = manifest.Template("cha")
    templ.add_data("Description", "win:AnsiString")
    p.add(templ)

    channel = manifest.Channel("kchaw")
    p.add(channel)

    ev = manifest.Event("pork",
        channel = channel,
        task = task,
        opcode = op,
        keywords = kw,
        level = lev,
        template = templ
        )
    p.add(ev)

    ev = manifest.Event("pork2",
        template = templ
        )
    p.add(ev)


    with open('test.man', 'w') as file:
        file.write(manifest_generator.to_manifest_xml([p]))

    profile_1 = manifest.Profile("General", "Sweet test profile")
    profile_1.add(p)

    with open('test.wprp', 'w') as file:
        file.write(wprp_generator.to_wprp_xml([profile_1]))
