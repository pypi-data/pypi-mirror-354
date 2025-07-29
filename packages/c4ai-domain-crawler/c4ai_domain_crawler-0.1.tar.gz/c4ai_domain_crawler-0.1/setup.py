from setuptools import setup, find_packages

setup(
    name="c4ai-domain-crawler",
    version="0.1",
    packages=find_packages(),
    install_requires=["aiohttp","crawl4ai","torch-snippets"],  # Add dependencies if needed
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "domain-crawler=c4ai_domain_crawler.domain_crawler:cli_entry"
        ]
    },
)
