ME=`pwd`
cd $ME/docs
make clean
make html
make json
make clean
cd $ME
python setup.py clean

python setup.py --long-description | rst2html.py --halt=3 > /dev/null
[ $? -ne 0 ] && exit;

python setup.py test

rm -rf dist
rm -rf django_helpfulfields*.egg-info
rm -rf django_setuptest-*.egg pep8-*.egg argparse-*.egg coverage-*.egg
rm -rf pep8.txt coverage.xml

python setup.py sdist --formats=tar,gztar,bztar,zip
python setup.py check
