# Generated by rust2rpm 27
%bcond check 1

%global crate laurel

Name:           rust-laurel
Version:        0.6.3
Release:        %autorelease
Summary:        Transform Linux Audit logs for SIEM usage

License:        GPL-3.0-or-later
URL:            https://crates.io/crates/laurel
Source:         %{crates_source}
# * Defines user to be added for LAUREL.
Source3:        rust-laurel.sysusers
# Manually created patch for downstream crate metadata changes
# * remove unused benchmark-only dependencies
Patch:          laurel-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  systemd-rpm-macros

%global _description %{expand:
LAUREL is an event post-processing plugin for auditd(8) that transforms and enriches audit logs to improve their utility for modern security monitoring setups.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
# FIXME: paste output of %%cargo_license_summary here
License:        # FIXME
# LICENSE.dependencies contains a full license breakdown

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%license LICENSE.dependencies
%doc INSTALL.md
%doc README.md
%doc performance.md
%{_bindir}/laurel
%{_bindir}/laurel2audit
%{_sysusersdir}/rust-laurel.conf

%package        devel
Summary:        %{summary}
BuildArch:      noarch
Requires:       audit

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/INSTALL.md
%doc %{crate_instdir}/README.md
%doc %{crate_instdir}/performance.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+procfs-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+procfs-devel %{_description}

This package contains library source intended for building other packages which
use the "procfs" feature of the "%{crate}" crate.

%files       -n %{name}+procfs-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%sysusers_create_compat %{SOURCE3}
%cargo_install
# sysusers
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/rust-laurel.conf

%if %{with check}
%check
%cargo_test
%endif

%changelog
%autochangelog
