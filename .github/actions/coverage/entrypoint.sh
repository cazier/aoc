#!/bin/sh

curl https://uploader.codecov.io/verification.gpg | gpg --no-default-keyring --keyring trustedkeys.gpg --import

cd /tmp
curl -Os https://uploader.codecov.io/latest/linux/codecov
curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM
curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM.sig
gpgv codecov.SHA256SUM.sig codecov.SHA256SUM
sha256sum -c codecov.SHA256SUM

chmod +x codecov

if [ "$INPUT_DRY_RUN" == "true" ]; then
    ./codecov -R $GITHUB_WORKSPACE -t $INPUT_SECRET -f $GITHUB_WORKSPACE/$INPUT_COVERAGE_FILE -d
else
    ./codecov -R $GITHUB_WORKSPACE -t $INPUT_SECRET -f $GITHUB_WORKSPACE/$INPUT_COVERAGE_FILE
fi
