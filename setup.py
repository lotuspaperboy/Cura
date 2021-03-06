# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.

from distutils.core import setup
import py2exe
import UM
import UM.Qt
import os
import re
import shutil
import site

# work around the limitation that shutil.copytree does not allow the target directory to exist
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

includes = ["sip", "ctypes", "UM", "PyQt5.QtNetwork", "PyQt5._QOpenGLFunctions_2_0", "serial", "Arcus", "google", "google.protobuf", "google.protobuf.descriptor", "xml.etree", "xml.etree.ElementTree", "src"]
# Include all the UM modules in the includes. As py2exe fails to properly find all the dependencies due to the plugin architecture.
for dirpath, dirnames, filenames in os.walk(os.path.dirname(UM.__file__)):
    if "__" in dirpath:
        continue
    module_path = dirpath.replace(os.path.dirname(UM.__file__), "UM")
    module_path = module_path.split(os.path.sep)
    module_name = ".".join(module_path)
    if os.path.isfile(dirpath + "/__init__.py"):
        includes += [module_name]
        for filename in filenames:
            if "__" in filename or not filename.endswith(".py"):
                continue
            includes += [module_name + "." + os.path.splitext(filename)[0]]

print("Removing previous distribution package")
shutil.rmtree("dist", True)

setup(name="Cura",
        version="2.0",
        author="Ultimaker",
        author_email="d.braam@ultimaker.com",
        url="http://software.ultimaker.com/",
        license="GNU AFFERO GENERAL PUBLIC LICENSE (AGPL)",
        scripts=["cura_app.py"],
        #windows=[{"script": "printer.py", "dest_name": "Cura"}],
        console=[{"script": "cura_app.py"}],
        options={"py2exe": {"skip_archive": False, "includes": includes}})

print("Coping Cura plugins.")
shutil.copytree(os.path.dirname(UM.__file__) + "/../plugins", "dist/plugins")
for path in os.listdir("plugins"):
	shutil.copytree("plugins/" + path, "dist/plugins/" + path)
print("Coping resources.")
shutil.copytree(os.path.dirname(UM.__file__) + "/../resources", "dist/resources")
copytree("resources", "dist/resources")
print("Coping Uranium QML.")
shutil.copytree(os.path.dirname(UM.__file__) + "/Qt/qml/UM", "dist/qml/UM")
for site_package in site.getsitepackages():
    qt_origin_path = os.path.join(site_package, "PyQt5")
    if os.path.isdir(qt_origin_path):
        print("Coping PyQt5 plugins from: %s" % qt_origin_path)
        shutil.copytree(os.path.join(qt_origin_path, "plugins"), "dist/PyQt5/plugins")
        print("Coping PyQt5 QtQuick from: %s" % qt_origin_path)
        shutil.copytree(os.path.join(qt_origin_path, "qml/QtQuick"), "dist/qml/QtQuick")
        shutil.copytree(os.path.join(qt_origin_path, "qml/QtQuick.2"), "dist/qml/QtQuick.2")
        print("Coping PyQt5 svg library from: %s" % qt_origin_path)
        shutil.copy(os.path.join(qt_origin_path, "Qt5Svg.dll"), "dist/Qt5Svg.dll")
