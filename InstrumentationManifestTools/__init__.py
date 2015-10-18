
def sample():
    p = Provider("Multi-Main")

    task = Task("task1")
    p.add(task)

    op = Opcode("opcode")
    p.add(op)

    kw = Keyword("kw")
    p.add(kw)

    filter = Filter("fil")
    p.add(filter)

    lev = Level("lev")
    p.add(lev)

    templ = Template("cha")
    templ.add_data("Description", "win:AnsiString")
    p.add(templ)

    channel = Channel("kchaw")
    p.add(channel)

    ev = Event("pork",
        channel = channel,
        task = task,
        opcode = op,
        keywords = kw,
        level = lev,
        template = templ
        )
    p.add(ev)

    ev = Event("pork2",
        template = templ
        )
    p.add(ev)


    with open('test.man', 'w') as file:
        file.write(to_manifest_xml([p]))

    profile_1 = Profile("General", "Sweet test profile")
    profile_1.add(p)

    with open('test.wprp', 'w') as file:
        file.write(to_wprp_xml([profile_1]))
