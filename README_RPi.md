# MediaPipe Python on aarch64 Ubuntu 20.04

*[Experimental] Only tested on Raspberry Pi 4 and Jeton Xavier NX.*

Based on: <https://github.com/jiuqiant/mediapipe_python_aarch64>

## Step to build MediaPipe Python on aarch64 Ubuntu 20.04

1. Clone [the MediaPipe repo](https://github.com/PincarBR/mediapipe)

2. Setup Bazelisk:  
    - Download latest `bazelisk-linux-arm64` binary from <https://github.com/bazelbuild/bazelisk/releases>  
    - Make the script executable: `chmod +x bazelisk-linux-arm64`  
    - Move it to `/usr/local/bin` renamed as bazel: `mv bazelisk-linux-arm64 /usr/local/bin/bazel`  

3. Install build dependencies.

    ```bash
    sudo apt install -y python3-dev
    sudo apt install -y cmake
    sudo apt install -y g++
    ```

4. Install proto compiler.

    ```bash
    sudo apt install -y protobuf-compiler
    ```

    If you see a missing any.proto error later, which means the protoc might be
    too old, you can download the latest protoc-3.x.x-linux-aarch_64.zip from
    [GitHub](https://github.com/protocolbuffers/protobuf/releases) and copy the
    "bin" and "include/google" directories to the system libraries. Then, modify
    `mediapipe/setup.py` like the following:

    ```python
    diff --git a/setup.py b/setup.py
    index 61848de..462d91d 100644
    --- a/setup.py
    +++ b/setup.py
    @@ -208,7 +208,7 @@ class GeneratePyProtos(setuptools.Command):
             sys.stderr.write('cannot find required file: %s\n' % source)
             sys.exit(-1)

    -      protoc_command = [self._protoc, '-I.', '--python_out=.', source]
    +      protoc_command = [self._protoc, '-I.', '-I/usr/local/include', '--python_out=.', source]
           if subprocess.call(protoc_command) != 0:
             sys.exit(-1)

    ```

5. Go to the MediaPipe directory.

    ```bash
    cd mediapipe
    ```

6. Remove unnecessary OpenCV modules and linker flags.

    ```bash
    sed -i -e "/\"imgcodecs\"/d;/\"calib3d\"/d;/\"features2d\"/d;/\"highgui\"/d;/\"video\"/d;/\"videoio\"/d" third_party/BUILD
    sed -i -e "/-ljpeg/d;/-lpng/d;/-ltiff/d;/-lImath/d;/-lIlmImf/d;/-lHalf/d;/-lIex/d;/-lIlmThread/d;/-lrt/d;/-ldc1394/d;/-lavcodec/d;/-lavformat/d;/-lavutil/d;/-lswscale/d;/-lavresample/d" third_party/BUILD
    ```

7. Disable carotene_o4t in `third_party/BUILD`.

    ```BUILD
    diff --git a/third_party/BUILD b/third_party/BUILD
    index ef408e4..51e1104 100644
    --- a/third_party/BUILD
    +++ b/third_party/BUILD
    @@ -110,6 +104,8 @@ cmake_external(
       "WITH_ITT": "OFF",
       "WITH_JASPER": "OFF",
       "WITH_WEBP": "OFF",
    +   "ENABLE_NEON": "OFF",
    +   "WITH_TENGINE": "OFF",
    ```

8. Install `numpy`

    ```bash
    pip3 install numpy
    ```

9. Build the package.

    ```bash
    python3 setup.py gen_protos && python3 setup.py bdist_wheel
    ```

10. Install MediaPipe package on the desired virtual env.

    ```bash
    python3 -m pip install mediapipe/dist/mediapipe-0.8-cp38-cp38-linux_aarch64.whl
    or 
    python3 -m pip install mediapipe-python-aarch64/mediapipe-0.8.4-cp38-cp38-linux_aarch64.whl
    ```

    Append `--no-deps` flag if any dependency Python packages cannot be installed.
