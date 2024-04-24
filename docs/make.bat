@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

if "%1" == "clean" goto build-sphinx-command

if "%2" == "rebuild" goto rebuild-api

:build-sphinx-command
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:rebuild-api
@REM rebuild specific package API documentation
echo Regenerating API documentation...
sphinx-apidoc -o source/generated/Asset ../src/tools/Asset --force --separate --no-headings --no-toc
sphinx-apidoc -o source/generated/Core ../src/tools/Core --force --separate --no-headings --no-toc
sphinx-apidoc -o source/generated/Rendering ../src/tools/Rendering --force --separate --no-headings --no-toc
sphinx-apidoc -o source/generated/Unreal ../src/tools/Unreal --force --separate --no-headings --no-toc
sphinx-apidoc -o source/generated/Util ../src/tools/Util --force --separate --no-headings --no-toc
goto build-sphinx-command

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
