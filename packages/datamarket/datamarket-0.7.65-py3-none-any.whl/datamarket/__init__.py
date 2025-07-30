from browserforge.download import Download, Remove, REMOTE_PATHS

# Monkey-patch the remote paths at runtime
REMOTE_PATHS["headers"] = (
    "https://raw.githubusercontent.com/apify/fingerprint-suite/667526247a519ec6fe7d99e640c45fbe403fb611/packages/header-generator/src/data_files"
)
REMOTE_PATHS["fingerprints"] = (
    "https://raw.githubusercontent.com/apify/fingerprint-suite/667526247a519ec6fe7d99e640c45fbe403fb611/packages/fingerprint-generator/src/data_files"
)

# Removes previously downloaded browserforge files if they exist
Remove()
# Downloads header and fingerprint definitions from the specified remote paths
Download(headers=True, fingerprints=True)
