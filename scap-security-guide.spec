%global		redhatssgversion	28

Name:		scap-security-guide
Version:	0.1.%{redhatssgversion}
Release:	3%{?dist}
Summary:	Security guidance and baselines in SCAP formats

Group:		System Environment/Base
License:	Public Domain
URL:		https://github.com/OpenSCAP/scap-security-guide

Source0:	%{name}-%{version}.tar.gz
Patch1:		scap-security-guide-0.1.27-document-kickstarts-in-manual-page.patch
Patch2:		scap-security-guide-0.1.27-downstream-use-internal-SSG-rpm-package-in-rhel6-kickstarts.patch
Patch3:		scap-security-guide-0.1.28-downstream-fix-multiple-issues-in-rhel6-smartcard-auth-remediation.patch
Patch4:		scap-security-guide-0.1.28-downstream-rhel6-audit-rules-privileged-commands-remediation.patch
Patch5:		scap-security-guide-0.1.28-backport-update-pci-dss-url.patch
Patch6:		scap-security-guide-0.1.28-rhel6-update-title-of-cnss-profile.patch
Patch7:		scap-security-guide-0.1.28-downstream-drop-install-hids-from-pci-dss.patch
Patch8:		scap-security-guide-0.1.28-rhel6-rhel7-add-computenode-cpe.patch
BuildArch:	noarch

BuildRequires:	libxslt, expat, python, openscap-scanner >= 1.0.10-2, python-lxml
Requires:	xml-common, openscap-scanner >= 1.0.10-2

%description
The scap-security-guide project provides a guide for configuration of the
system from the final system's security point of view. The guidance is
specified in the Security Content Automation Protocol (SCAP) format and
constitutes a catalog of practical hardening advice, linked to government
requirements where applicable. The project bridges the gap between generalized
policy requirements and specific implementation guidelines. The Red Hat
Enterprise Linux 6 system administrator can use the oscap command-line tool
from the openscap-scanner package to verify that the system conforms to provided
guideline. Refer to scap-security-guide(8) manual page for further information.

%package        doc
Summary:        HTML formatted documents containing security guides generated from XCCDF benchmarks.
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains HTML formatted documents containing security guides that have
been generated from XCCDF benchmarks present in %{name} package.

%prep
%setup -q -n %{name}-%{version}
# Downstream patches
%patch1 -p1 -b .document_kickstarts_in_manual_page
%patch2 -p1 -b .use_internal_ssg_rpm_in_kickstarts
%patch3 -p1 -b .rhel6_smartcard_auth_fix
%patch4 -p1 -b .rhel6_audit_rules_priv_commands_fix
%patch5 -p5 -b .update_pci_dss_url
%patch6 -p1 -b .rhel6_update_cnss_profile_title
%patch7 -p1 -b .drop_install_hids_rule_from_pci_dss
%patch8 -p1 -b .rhel6_rhel7_add_computenode_cpe

%build
(cd RHEL/6 && make dist)
(cd RHEL/7 && make dist)
(cd Firefox && make dist)
(cd JRE && make dist)

%install

rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/xml/scap/ssg/content
mkdir -p %{buildroot}%{_mandir}/en/man8/

# Add in RHEL-6 core content (SCAP)
cp -a RHEL/6/dist/content/ssg-rhel6-cpe-dictionary.xml %{buildroot}%{_datadir}/xml/scap/ssg/content/
cp -a RHEL/6/dist/content/ssg-rhel6-cpe-oval.xml %{buildroot}%{_datadir}/xml/scap/ssg/content/
cp -a RHEL/6/dist/content/ssg-rhel6-ds.xml %{buildroot}%{_datadir}/xml/scap/ssg/content/
cp -a RHEL/6/dist/content/ssg-rhel6-oval.xml %{buildroot}%{_datadir}/xml/scap/ssg/content/
cp -a RHEL/6/dist/content/ssg-rhel6-xccdf.xml %{buildroot}%{_datadir}/xml/scap/ssg/content/

# Add in RHEL-7 datastream (SCAP)
cp -a RHEL/7/dist/content/ssg-rhel7-ds.xml %{buildroot}%{_datadir}/xml/scap/ssg/content

# Add in Firefox datastream (SCAP)
cp -a Firefox/dist/content/ssg-firefox-ds.xml %{buildroot}%{_datadir}/xml/scap/ssg/content

# Add in Java Runtime Environment (JRE) datastream (SCAP)
cp -a JRE/dist/content/ssg-jre-ds.xml %{buildroot}%{_datadir}/xml/scap/ssg/content

# Add in library for remediations
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a shared/remediations/bash/templates/remediation_functions %{buildroot}%{_datadir}/%{name}/remediation_functions

# Add in RHEL-6 kickstart files
mkdir -p %{buildroot}%{_datadir}/%{name}/kickstart
cp -a RHEL/6/kickstart/ssg-rhel6-usgcb-server-with-gui-ks.cfg %{buildroot}%{_datadir}/%{name}/kickstart/ssg-rhel6-usgcb-server-with-gui-ks.cfg
cp -a RHEL/6/kickstart/ssg-rhel6-stig-ks.cfg %{buildroot}%{_datadir}/%{name}/kickstart/ssg-rhel6-stig-ks.cfg
cp -a RHEL/6/kickstart/ssg-rhel6-pci-dss-with-gui-ks.cfg %{buildroot}%{_datadir}/%{name}/kickstart/ssg-rhel6-pci-dss-with-gui-ks.cfg 

# Add in manpage
cp -a docs/scap-security-guide.8 %{buildroot}%{_mandir}/en/man8/scap-security-guide.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/xml/scap
%{_datadir}/%{name}
%lang(en) %{_mandir}/en/man8/scap-security-guide.8.gz
%doc LICENSE RHEL/6/output/table-rhel6-cces.html RHEL/6/output/table-rhel6-nistrefs-common.html RHEL/6/output/table-rhel6-nistrefs.html RHEL/6/output/table-rhel6-srgmap-flat.html RHEL/6/output/table-rhel6-srgmap-flat.xhtml RHEL/6/output/table-rhel6-srgmap.html RHEL/6/output/table-rhel6-stig.html RHEL/6/input/auxiliary/DISCLAIMER

%files doc
%defattr(-,root,root,-)
%doc RHEL/6/output/ssg-rhel6-guide-*.html RHEL/7/output/ssg-rhel7-guide-*.html JRE/output/ssg-jre-guide-*.html Firefox/output/ssg-firefox-guide-*.html

%changelog
* Mon Nov 07 2016 Watson Sato <wsato@redhat.com> 0.1.28-3
- Add ComputeNode CPE for RHEL 6 and 7 (RH BZ#1311054)

* Thu Feb 04 2016 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.28-2
- Update URL to PCI DSS standard (latest version is v3.1 from April 2015)
- Enhance title of CNSS No.1253 profile for Red Hat Enterprise Linux 6
  (RH BZ#1284045#c8)
- Drop 'install_hids' rule from PCI DSS profile for both Red Hat Enterprise
  Linux 6 and 7 (since we don't have an OVAL check for this requirement)

* Tue Jan 19 2016 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.28-1
- Rebase to upstream 0.1.28 version
- Start using consistent IDs for OVAL definitions (RH BZ#1250808)

* Tue Dec 15 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.27-2
- Modify the upstream provided kickstart files for Red Hat Enterprise Linux 6
  to use internal scap-security-guide RPM package rather than upstream git
  repository copies (RH BZ#1251929)

* Tue Dec 15 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.27-1
- Rebase to upstream 0.1.27 version (RH BZ#1267509, RH BZ#1284045,
  RH BZ#1270329, RH BZ#1250895, RH BZ#1270710, RH BZ#1223865)
- Perform the spec changes necessary for the rebase:
  * Update path to remediation functions library, list of provided
  kickstart files, path to scap-security-guide(8) manual page, path
  to LICENSE file
  * Drop:
  - scap-security-guide-0.1.21-dev-shm-removable.patch
  - scap-security-guide-0.1.21-dont-include-the-test-profile.patch
  patches since they have been merged upstream
  * Replace:
  - scap-security-guide-0.1.21-document-kickstart-in-manual-page.patch
  with its updated:
  - scap-security-guide-0.1.27-document-kickstarts-in-manual-page.patch
  version to also document inclusion of new kickstart files for Red Hat
  Enterprise Linux 6 that are available in upstream's 0.1.27 release
  * Introduce the new scap-security-guide-doc subpackage (to contain the
  HTML formatted documents containing security guides that have been
  generated from XCCDF benchmarks present in the scap-security-guide package)
  * Include the datastream versions of Firefox and Java Runtime Environment
  (JRE) benchmarks

* Tue Dec 15 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.21-4
- Update R / BR to lightweight openscap-scanner >= 1.0.10-2 package
  (RH BZ#1243396)
- Update URL to point to official SCAP Security Guide GitHub repository

* Tue May 12 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.21-3
- Rebuild scap-security-guide RPM against openscap >= 1.0.9 in order the
  upstream SCAP Security Guide logo to be rendered properly in the generated
  HTML guide

* Mon Mar 09 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.21-2
- Re-implement nodev, noexec, and nosuid removable media OVAL checks
  (RH BZ#1185426)
- Don't include the 'test' profile into the SCAP content (RH BZ#1199946)
- Document USGCB profile kickstart availability for Red Hat Enterprise Linux 6
  in the scap-security-guide manual page (RH BZ#1133963)

* Fri Feb 20 2015 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.21-1
- Upgrade to upstream 0.1.21 version
- Drop C2S profile patch since it has been adopted upstream
- Include datastream forms of benchmarks for Red Hat Enterprise Linux 6
  and Red Hat Enterprise Linux 7
- Include the kickstart file for United States Government Configuration
  Baseline (USGCB) profile for Red Hat Enterprise Linux 6

* Thu Aug 28 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.18-3
- Update C2S profile <description> per request from CIS

* Thu Jun 26 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.18-2
- Include the upstream STIG for RHEL 6 Server profile disclaimer file too

* Sun Jun 22 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.18-1
- Make new 0.1.18 release

* Wed May 14 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.17-2
- Drop vendor line from the spec file. Let the build system to provide it.

* Fri May 09 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.17-1
- Upgrade to upstream 0.1.17 version

* Mon May 05 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.16-2
- Initial RPM for RHEL base channels

* Mon May 05 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.16-1
- Change naming scheme (0.1-16 => 0.1.16-1)

* Fri Feb 21 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-16
- Include datastream file into RHEL6 RPM package too
- Bump version

* Tue Dec 24 2013 Shawn Wells <shawn@redhat.com> 0.1-16.rc2
+ RHEL6 stig-rhel6-server XCCDF profile renamed to stig-rhel6-server-upstream

* Mon Dec 23 2013 Shawn Wells <shawn@redhat.com> 0.1-16.rc1
- [bugfix] RHEL6 no_empty_passwords remediation script overwrote
  system-auth symlink. Added --follow-symlink to sed command.

* Fri Nov 01 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-15
- Version bump

* Sat Oct 26 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-15.rc5
- Point the spec's source to proper remote tarball location
- Modify the main Makefile to use remote tarball when building RHEL/6's SRPM

* Sat Oct 26 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-15.rc4
- Don't include the table html files two times
- Remove makewhatis

* Fri Oct 25 2013 Shawn Wells <shawn@redhat.com> 0.1-15.rc3
- [bugfix] Updated rsyslog_remote_loghost to scan /etc/rsyslog.conf and /etc/rsyslog.d/*
- Numberous XCCDF->OVAL naming schema updates
- All rules now have CCE

* Fri Oct 25 2013 Shawn Wells <shawn@redhat.com> 0.1-15.rc2
- RHEL/6 HTML table naming bugfixes (table-rhel6-*, not table-*-rhel6)

* Fri Oct 25 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-15.rc1
- Apply spec file changes required by review request (RH BZ#1018905)

* Thu Oct 24 2013 Shawn Wells <shawn@redhat.com> 0.1-14
- Formal RPM release
- Inclusion of rht-ccp profile
- OVAL unit testing patches
- Bash remediation patches
- Bugfixes

* Mon Oct 07 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-14.rc1
- Change RPM versioning scheme to include release into tarball

* Sat Sep 28 2013 Shawn Wells <shawn@redhat.com> 0.1-13
- Updated RPM spec file to fix rpmlint warnings

* Wed Jun 26 2013 Shawn Wells <shawn@redhat.com> 0.1-12
- Updated RPM version to 0.1-12

* Fri Apr 26 2013 Shawn Wells <shawn@redhat.com> 0.1-11
- Significant amount of OVAL bugfixes
- Incorporation of Draft RHEL/6 STIG feedback

* Sat Feb 16 2013 Shawn Wells <shawn@redhat.com> 0.1-10
- `man scap-security-guide`
- OVAL bug fixes
- NIST 800-53 mappings update

* Wed Nov 28 2012 Shawn Wells <shawn@redhat.com> 0.1-9
- Updated BuildRequires to reflect python-lxml (thank you, Ray S.!)
- Reverting to noarch RPM

* Tue Nov 27 2012 Shawn Wells <shawn@redhat.com> 0.1-8
- Significant copy editing to XCCDF rules per community
  feedback on the DISA RHEL/6 STIG Initial Draft

* Thu Nov 1 2012 Shawn Wells <shawn@redhat.com> 0.1-7
- Corrected XCCDF content errors
- OpenSCAP now supports CPE dictionaries, important to
  utilize --cpe-dict when scanning machines with OpenSCAP,
  e.g.:
  $ oscap xccdf eval --profile stig-server \
   --cpe-dict ssg-rhel6-cpe-dictionary.xml ssg-rhel6-xccdf.xml

* Mon Oct 22 2012 Shawn Wells <shawn@redhat.com> 0.1-6
- Corrected RPM versioning, we're on 0.1 release 6 (not version 1 release 6)
- Updated RPM includes feedback received from DoD Consensus meetings

* Fri Oct 5  2012 Jeffrey Blank <blank@eclipse.ncsc.mil> 1.0-5
- Adjusted installation directory to /usr/share/xml/scap.

* Tue Aug 28  2012 Spencer Shimko <sshimko@tresys.com> 1.0-4
- Fix BuildRequires and Requires.

* Tue Jul 3 2012 Jeffrey Blank <blank@eclipse.ncsc.mil> 1.0-3
- Modified install section, made description more concise.

* Thu Apr 19 2012 Spencer Shimko <sshimko@tresys.com> 1.0-2
- Minor updates to pass some variables in from build system.

* Mon Apr 02 2012 Shawn Wells <shawn@redhat.com> 1.0-1
- First attempt at SSG RPM. May ${deity} help us...
