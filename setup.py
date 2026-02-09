from setuptools import setup, find_packages

setup(
    name="pretix-plugin-advanced-stats",
    version="0.1.0",
    description="Advanced(ish) stats for Pretix",
    author="Ernesto Arbitrio",
    author_email="ernesto.arbitrio@gmail.com",
    packages=find_packages(),
    install_requires=["pretix"],
    entry_points={
        "pretix.plugin": [
            "pretix_advanced_stats = pretix_advanced_stats:PretixPluginMeta",
        ],
    },
)
