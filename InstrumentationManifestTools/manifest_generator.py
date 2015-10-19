import InstrumentationManifestTools.simple_xml as xml
import re


def make_symbol(*args):
    return re.sub('[^0-9A-Z]+', '_', '_'.join(args).upper())


def to_manifest_xml(providers):
    root = xml.Node(
        'instrumentationManifest',
        xmlns="http://schemas.microsoft.com/win/2004/08/events"
    )

    instrumentation = root.add('instrumentation')
    instrumentation.attrs({
        'xmlns:win': "http://manifests.microsoft.com/win/2004/08/windows/events",
        'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"
    })

    container_root = instrumentation.add('events')
    container_root.attrs(xmlns="http://schemas.microsoft.com/win/2004/08/events")

    for p in providers:
        provider = container_root.add('provider',
                                      name=p.name,
                                      symbol=make_symbol(p.name),
                                      guid=p.guid,
                                      messageFileName=p.binary_filename,
                                      resourceFileName=p.binary_filename
                                      )

        def build_container(provider, xml, name, build):
            cnt = p.container(name)
            xml_cnt = provider.add(name + 's')
            for o in cnt:
                xml = xml_cnt.add(name)

                build(xml, o)

        def build_event(xml, evt):
            xml.attrs(
                symbol=make_symbol(p.name, "event", evt.name),
                template=evt.template.name if evt.template else None,
                value=evt.value,
                level=evt.level.name if evt.level else None,
                channel=evt.channel.name if evt.channel else None,
                task=evt.task.name if evt.task else None,
                opcode=evt.opcode.name if evt.opcode else None,
                keywords=evt.keywords.name if evt.keywords else None,
                message=evt.message
            )

        build_container(provider, p, 'event', build_event)

        def build_task(xml, task):
            xml.attrs(
                name=task.name,
                symbol=make_symbol(p.name, "task", task.name),
                value=task.value,
                message=task.message
            )

        build_container(provider, p, 'task', build_task)

        def build_opcode(xml, opcode):
            xml.attrs(
                name=opcode.name,
                symbol=make_symbol(p.name, "opcode", opcode.name),
                value=opcode.value,
                message=opcode.message
            )

        build_container(provider, p, 'opcode', build_opcode)

        def build_keyword(xml, keyword):
            xml.attrs(
                name=keyword.name,
                mask=keyword.mask
            )

        build_container(provider, p, 'keyword', build_keyword)

        def build_filter(xml, filter):
            xml.attrs(
                name=filter.name,
                value=filter.value,
                tid=filter.template.name if filter.template else None,
                symbol=make_symbol(p.name, "filter", filter.name),
            )

        build_container(provider, p, 'filter', build_filter)

        def build_level(xml, level):
            xml.attrs(
                name=level.name,
                value=level.value,
                symbol=make_symbol(p.name, "level", level.name),
                message=level.message
            )

        build_container(provider, p, 'level', build_level)

        def build_channel(xml, channel):
            xml.attrs(
                chid=channel.name,
                name="{}/{}".format(channel.name, channel.type),
                type=channel.type,
                enabled=channel.enabled
            )

        build_container(provider, p, 'channel', build_channel)

        def build_template(xml, template):
            xml.attrs(
                tid=template.name
            )

            for d in template.data:
                data_xml = xml.add(
                    'data',
                    name=d[0],
                    inType=d[1]
                )

        build_container(provider, p, 'template', build_template)

    return root.to_xml_document()
