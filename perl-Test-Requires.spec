%{?scl:%scl_package perl-Test-Requires}

Name:		%{?scl_prefix}perl-Test-Requires
Summary:	Checks to see if a given module can be loaded
Version:	0.10
Release:	5%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Requires
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-Requires-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.64
# Module
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(Test::Builder::Module)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(Data::Dumper)
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.47
# Extra Tests
%if 0%{!?perl_bootstrap:1} && !%{defined perl_small}
# Test::Perl::Critic -> Perl::Critic -> PPIx::Regexp -> Test::Kwalitee ->
#   Module::CPANTS::Analyse -> Test::Warn -> Sub::Uplevel -> Pod::Wordlist::hanekomu -> Test::Requires
BuildRequires:	%{?scl_prefix}perl(Test::Perl::Critic)
%endif
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))

%description
Test::Requires checks to see if the module can be loaded.

If this fails, rather than failing tests this skips all tests.

%prep
%setup -q -n Test-Requires-%{version}

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
# note the "skipped" warnings indicate success :)
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%{?scl:scl enable %{scl} '}make test TEST_FILES="xt/*.t"%{?scl:'}

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%doc LICENSE
%else
%doc LICENSE
%endif
%doc Changes README.md t/ xt/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Requires.3*

%changelog
* Wed Jul 13 2016 Petr Pisar <ppisar@redhat.com> - 0.10-5
- SCL

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-4
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10
  - Support 5.6 again

* Tue Jul 21 2015 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Requires 5.8.1
- Use %%doc where possible

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-5
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-4
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-2
- Perl 5.20 rebuild

* Wed Jul 16 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Switch to ExtUtils::MakeMaker

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Petr Pisar <ppisar@redhat.com> - 0.07-5
- Specify all dependencies (bug #1066077)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.07-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.07-2
- Perl 5.18 rebuild

* Mon Jul  1 2013 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - If the RELEASE_TESTING environment variable is true, then instead of
    skipping tests, Test::Requires bails out
  - Document that use Test::Requires "5.010" works
- Switch to Module::Build flow
- Classify buildreqs by usage
- Package upstream's new LICENSE and README.md files
- Drop obsoletes/provides of perl-Test-Requires-tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.06-9
- BR: perl(base), perl(Cwd), perl(Data::Dumper)
- RHEL builds don't use Test::Spelling so they don't need dictionaries either

* Wed Aug 15 2012 Marcela Maslanova <mmaslano@redhat.com> - 0.06-8
- Conditionalize test packages

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.06-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.06-5
- Perl 5.16 rebuild

* Thu Mar 22 2012 Paul Howarth <paul@city-fan.org> - 0.06-4
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't need explicit runtime dependency on perl(Test::Builder::Module) if we
  have rpm ≥ 4.9 as it can auto-detect it
- BR: at least version 0.61 of perl(Test::More) as per upstream
- Drop unnecessary version requirement for perl(ExtUtils::MakeMaker)
- Drop redundant %%{?perl_default_filter}
- BR: aspell-en rather than hunspell-en on old distributions where
  Test::Spelling uses aspell instead of hunspell
- Don't BR: perl(Test::Perl::Critic) when bootstrapping
- Don't use macros for commands
- Don't need to remove empty directories from buildroot
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 0.06-3
- BR: hunspell-en rather than aspell-en (#731272)

* Thu Nov 18 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Run release tests as well as standard test suite in %%check
- Drop no-longer-needed buildreq perl(Filter::Util::Call)
- New buildreqs perl(Test::Perl::Critic), perl(Test::Pod), perl(Test::Spelling)

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> - 0.06-1
- Update to latest upstream version

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-2
- Mass rebuild with perl-5.12.0

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Specfile by Fedora::App::MaintainerTools 0.006


