%{?scl:%scl_package perl-Test-Requires}
%{!?scl:%global pkg_name %{name}}

# Only need manual requires for "use base XXX;" prior to rpm 4.9
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e')

Name:		%{?scl_prefix}perl-Test-Requires
Summary:	Checks to see if a given module can be loaded
Version:	0.07
Release:	2.sc1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Requires
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-Requires-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta)
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta::Prereqs)
BuildRequires:	%{?scl_prefix}perl(File::Basename)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(Module::Build) >= 0.38
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(utf8)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Module
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(Test::Builder::Module)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(Data::Dumper)
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.61
# Extra Tests
%if  0%{!?perl_bootstrap:1} && 0%{!?rhel:1}
# Test::Perl::Critic -> Perl::Critic -> PPIx::Regexp -> Test::Kwalitee ->
#   Module::CPANTS::Analyse -> Test::Warn -> Sub::Uplevel -> Pod::Wordlist::hanekomu -> Test::Requires
BuildRequires:	%{?scl_prefix}perl(Test::Perl::Critic)
%endif
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
%if ! %{rpm49}
Requires:	%{?scl_prefix}perl(Test::Builder::Module)
%endif

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	%{?scl_prefix}%{pkg_name}-tests < %{version}-%{release}
Provides:	%{?scl_prefix}%{pkg_name}-tests = %{version}-%{release}

%description
Test::Requires checks to see if the module can be loaded.

If this fails, rather than failing tests this skips all tests.

%prep
%setup -q -n Test-Requires-%{version}

%build
%{?scl:scl enable %{scl} "}
perl Build.PL installdirs=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
./Build
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
./Build install destdir=%{buildroot} create_packlist=0
%{?scl:"}

%check
# note the "skipped" warnings indicate success :)
%{?scl:scl enable %{scl} "}
./Build test
%{?scl:"}
%{?scl:scl enable %{scl} '}
./Build test --test_files="xt/*.t"
%{?scl:'}

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README.md t/ xt/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Requires.3pm*

%changelog
* Tue Feb 18 2014 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Specify all dependencies (bug #1066077)

* Wed Nov 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-1
- 0.07 bump

* Mon Mar 11 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-1
- SCL package - initial import
