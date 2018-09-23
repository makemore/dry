#!/bin/bash

./gradlew ${1:-installDevMinSdkDevKernelDebug} --stacktrace && adb shell am start -n com.makemoredigital.dry/host.exp.exponent.MainActivity
