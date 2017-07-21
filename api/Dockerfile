FROM tensorflow/syntaxnet
#If they ever update this image things will likely break

#y_tho.gif
ENV PYTHONPATH="${PYTHONPATH}:/opt/tensorflow/syntaxnet/bazel-bin/dragnn/tools/oss_notebook_launcher.runfiles/__main__:/opt/tensorflow/syntaxnet/bazel-bin/dragnn/tools/oss_notebook_launcher.runfiles/org_tensorflow"

ADD . /src
RUN pip install -r /src/requirements.txt

CMD ["python", "/src/app.py"]
