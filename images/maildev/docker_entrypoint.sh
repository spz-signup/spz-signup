#!/usr/bin/env bash

# PaX fix
# that needs to be done during container boot because attributes are not preserved by images
setfattr -n user.pax.flags -v "em" /usr/local/bin/node || true

# run payload
exec $@
