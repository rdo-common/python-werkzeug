%global srcname Werkzeug

Name:           python-werkzeug
Version:        0.12.2
Release:        2%{?dist}
Summary:        The Swiss Army knife of Python web development 

Group:          Development/Libraries
License:        BSD
URL:            http://werkzeug.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/W/Werkzeug/%{srcname}-%{version}.tar.gz
# Pypi version of werkzeug is missing _themes folder needed to build werkzeug sphinx docs
# See https://github.com/mitsuhiko/werkzeug/issues/761
Source1:        werkzeug-sphinx-theme.tar.gz

BuildArch:      noarch

%global _description\
Werkzeug\
========\
\
Werkzeug started as simple collection of various utilities for WSGI\
applications and has become one of the most advanced WSGI utility\
modules.  It includes a powerful debugger, full featured request and\
response objects, HTTP utilities to handle entity tags, cache control\
headers, HTTP dates, cookie handling, file uploads, a powerful URL\
routing system and a bunch of community contributed addon modules.\
\
Werkzeug is unicode aware and doesn't enforce a specific template\
engine, database adapter or anything else.  It doesn't even enforce\
a specific way of handling requests and leaves all that up to the\
developer. It's most useful for end user applications which should work\
on as many server environments as possible (such as blogs, wikis,\
bulletin boards, etc.).\


%description %_description

%package -n python2-werkzeug
Summary: %summary

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%{?python_provide:%python_provide python2-werkzeug}

%description -n python2-werkzeug %_description

%package -n python2-werkzeug-doc
Summary:        Documentation for %{name}

BuildRequires:  python2-sphinx

Requires:       python2-werkzeug = %{version}-%{release}
%{?python_provide:%python_provide python2-werkzeug-doc}

%description -n python2-werkzeug-doc
Documentation and examples for %{name}.


%package -n python3-werkzeug
Summary:        %summary

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%{?python_provide:%python_provide python3-werkzeug}

%description -n python3-werkzeug %_description


%package -n python3-werkzeug-doc
Summary:        Documentation for python3-werkzeug

BuildRequires:  python3-sphinx

Requires:       python3-werkzeug = %{version}-%{release}
%{?python_provide:%python_provide python3-werkzeug-doc}

%description -n python3-werkzeug-doc
Documentation and examples for python3-werkzeug.


%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i 's/\r//' LICENSE
%{__sed} -i '1d' tests/multipart/test_collect.py
tar -xf %{SOURCE1}

rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'


%build
%py2_build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
# Add a symlink to the dir with the Python module so that __version__ can be
# obtained therefrom.
ln -s ../werkzeug werkzeug
make html
popd

pushd %{py3dir}
%py3_build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
# Add a symlink to the dir with the Python module so that __version__ can be
# obtained therefrom.
ln -s ../werkzeug werkzeug
make html
popd
popd


%install
%py2_install
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc

pushd %{py3dir}
%py3_install
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc
popd

%files -n python2-werkzeug
%license LICENSE
%doc AUTHORS PKG-INFO CHANGES
%{python2_sitelib}/*

%files -n python2-werkzeug-doc
%doc docs/_build/html examples

%files -n python3-werkzeug
%license LICENSE
%doc AUTHORS PKG-INFO CHANGES
%{python3_sitelib}/*

%files -n python3-werkzeug-doc
%doc docs/_build/html examples


%changelog
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.12.2-1
- Update to 0.12.2

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.11.10-8
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11.10-7
- Python 2 binary package renamed to python2-werkzeug
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.11.10-4
- Rebuild for Python 3.6

* Tue Dec 13 2016 Tomas Orsava <torsava@redhat.com> - 0.11.10-3
- Fixed the building of documentation

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.10-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat May 28 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.11.10-1
- Upstream 0.11.19
- Fix unicode issues with python3

* Thu Apr 14 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.11.6-1
- Upstream 0.11.6 (upstream #822)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.10.4-3
- Rebuilt for Python3.5 rebuild
- Add werkzeug sphinx theme as a Source1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 30 2015 Ricky Elrod <relrod@redhat.com> - 0.10.4-1
- Upstream 0.10.4.

* Fri Jul 18 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.6-1
- Upstream 0.9.6
- Fixes RHBZ #1105819

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug 26 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.4-1
- Upstream 0.9.4

* Thu Jul 25 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.3-1
- Upstream 0.9.3

* Tue Jul 23 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.2-1
- Upstream 0.9.2 release.

* Sat Jun 15 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.1-1
- upstream 0.9.1
- add python3 flavor

* Fri Jun 14 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-1
- Upstream 0.9.0 release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.3-1
- upstream 0.8.3 (fixes XSS security issues)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.2-1
- upstream 0.8.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.2-1
- Updating because upstream release of Werkzeug 0.6.2

* Fri Mar 05 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6-1
- Updating because upstream release of Werkzeug 0.6

* Tue Aug 25 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.5.1-1
- Initial package
