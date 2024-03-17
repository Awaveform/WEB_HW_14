# WEB_HW_13
poetry add sphinx -G dev
sphinx-quickstart docs
cd docs
.\make.bat html

poetry add pytest
poetry add httpx -G test
