import yaml
import argparse

# # libvirt
# print(prometheus_org['scrape_configs'][0]['static_configs'][0]['targets'])
# # cube
# print(prometheus_org['scrape_configs'][1]['static_configs'][0]['targets'])
# # scvm
# print(prometheus_org['scrape_configs'][2]['static_configs'][0]['targets'])
# # ccvm
# print(prometheus_org['scrape_configs'][3]['static_configs'][0]['targets'])
# # prometheus
# print(prometheus_org['scrape_configs'][4]['static_configs'][0]['targets'])
# # cube-process-exporter
# print(prometheus_org['scrape_configs'][5]['static_configs'][0]['targets'])
# # scvm-process-exporter
# print(prometheus_org['scrape_configs'][6]['static_configs'][0]['targets'])
# # ccvm-process-exporter
# print(prometheus_org['scrape_configs'][7]['static_configs'][0]['targets'])
# # cube-blackbox-exporter
# print(prometheus_org['scrape_configs'][8]['static_configs'][0]['targets'])
# # scvm-blackbox-exporter
# print(prometheus_org['scrape_configs'][9]['static_configs'][0]['targets'])
# # ccvm-blackbox-exporter
# print(prometheus_org['scrape_configs'][10]['static_configs'][0]['targets'])
# # blackbox-tcp
# print(prometheus_org['scrape_configs'][11]['static_configs'][0]['targets'])

libvirt_exporter_port = ":3002"
node_exporter_port = ":3003"


def parseArgs():
    parser = argparse.ArgumentParser(description='Pacemaker cluster for Cloud Center VM',
                                     epilog='copyrightⓒ 2021 All rights reserved by ABLECLOUD™')

    parser.add_argument('action', choices=[
                        'config'], help='choose one of the actions')
    parser.add_argument('--cube', metavar='name', type=str,
                        nargs='*', help='Hostnames to form a cluster')
    parser.add_argument('--scvm', metavar='name', type=str,
                        nargs='*', help='Hostnames to form a cluster')
    parser.add_argument('--ccvm', metavar='name', type=str,
                        nargs='*', help='Hostnames to form a cluster')
    parser.add_argument('--prometheus', metavar='name', type=str,
                        nargs='*', help='Hostnames to form a cluster')

    return parser.parse_args()


def libvirt_config(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + libvirt_exporter_port
    return cube


def cube_node_config(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + node_exporter_port
    return cube


def scvm_node_config(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i] + node_exporter_port
    return scvm


def ccvm_node_config(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + node_exporter_port
    return ccvm


def configYaml(cube, scvm, ccvm):
    with open('prometheus_org.yml') as f:
        prometheus_org = yaml.load(f, Loader=yaml.FullLoader)

    for i in range(len(prometheus_org['scrape_configs'])):
        if i == 0:
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = libvirt_config(
                cube)

            print(prometheus_org['scrape_configs'][0]
                  ['static_configs'][0]['targets'])

        elif i == 1:
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cube_node_config(
                cube)

            print(prometheus_org['scrape_configs'][1]
                  ['static_configs'][0]['targets'])

        elif i == 2:
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = scvm_node_config(
                scvm)

            print(prometheus_org['scrape_configs'][2]
                  ['static_configs'][0]['targets'])

        elif i == 3:
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = ccvm_node_config(
                ccvm)

            print(prometheus_org['scrape_configs'][3]
                  ['static_configs'][0]['targets'])


# prometheus_org['scrape_configs'][0]['static_configs'][0]['targets'] = ['10.10.1.3:3002', '10.10.1.2:3002', '10.10.1.1:3002']
# with open('prometheus_test.yml', 'w') as yaml_file:
#     yaml_file.write(yaml.dump(prometheus_org, default_flow_style=False))
if __name__ == "__main__":
    args = parseArgs()
    # if (args.action) == 'config':
    #     configYaml(args.cube)
    if (args.action) == 'config':
        configYaml(args.cube, args.scvm, args.ccvm)
