

# mount data dir onto image to run it and have the data already in there

docker run \
  --volume /data/mince/stables:/data/mince/stables \
  --publish 8056:8056 \
  mince-stables \
  --verbose --other-flag value
