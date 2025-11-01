from sb_cfg_gen.lib import get_minecraft_instances


def main():
    print("Hello, Minecraft Cli")
    for instance in get_minecraft_instances():
        print(instance)


if __name__ == "__main__":
    main()