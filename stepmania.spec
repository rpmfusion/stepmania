Name:          stepmania

%global        forgeurl https://github.com/stepmania/stepmania
%global        version0 5.1.0
%global        commit   d55acb1ba26f1c5b5e3048d6d6c0bd116625216f

%forgemeta

# This is hardcoded in src/CMakeLists.txt as SM_INSTALL_DESTINATION:
%global        main_version 5.1

# Note that we do not use _datadir here, even though most of the_data_directory content
# is arch-independent. Stepmania supports single data directory only, determined by the
# dirname of argv[0] (hence the shell wrapper in _bindir below), and the data directory
# contains also an arch-dependent file GtkModule.so. So I think it is cleaner
# to have the_data_directory under _libdir:
%global        the_data_directory %{_libdir}/%{name}-%{main_version}

Version:       %forgeversion -p
Release:       5%{?dist}
Group:         Amusements/Games
Summary:       Advanced cross-platform rhythm game
URL:           %{forgeurl}
# See README.md for licensing info: everything is under MIT except three mp3/ogg songs
# under the_data_directory/Songs/StepMania 5/, which are under CC-BY-NC.
License:       MIT AND CC-BY-NC-4.0

# wget -O stepmania-$COMMIT.tar.gz https://github.com/stepmania/stepmania/archive/stepmania-$COMMIT.tar.gz
Source0:       %{forgesource}

# Most patches and cmake invocation taken from Arch Linux build of Stepmania:
# https://aur.archlinux.org/packages/stepmania

Patch1:        https://github.com/stepmania/stepmania/commit/e0d2a5182dcd855e181fffa086273460c553c7ff.patch#/stepmania-fix-preview-crash.patch
Patch2:        https://github.com/stepmania/stepmania/commit/3fef5ef60b7674d6431f4e1e4ba8c69b0c21c023.patch#/stepmania-fix-ffmpeg-avcodec.patch
Patch3:        https://aur.archlinux.org/cgit/aur.git/plain/ffmpeg-remove-asm-requirement.patch?h=stepmania#/stepmania-remove-ffmpeg-asm-requirement.patch
Patch4:        https://aur.archlinux.org/cgit/aur.git/plain/ffmpeg-7.patch?h=stepmania#/stepmania-ffmeg-frame-num.patch
Patch5:        stepmania-long-musicwheel.patch

# The code doesn’t recognize the ppc64le architecture
# archutils/Common/PthreadHelpers.cpp:251:2  error: #error GetThreadBacktraceContext: which arch?
ExcludeArch:   ppc64le

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: desktop-file-utils

BuildRequires: alsa-lib-devel
BuildRequires: bzip2-devel
BuildRequires: ffmpeg-devel
BuildRequires: glew-devel
BuildRequires: glibc-devel
BuildRequires: jsoncpp-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libmad-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: libtomcrypt-devel
BuildRequires: libtommath-devel
BuildRequires: libvorbis-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXtst-devel
BuildRequires: pcre-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: systemd-devel

# from README.md:
%description
StepMania is a free dance and rhythm game for Windows, Mac, and Linux.
It features 3D graphics, keyboard and "dance pad" support, and an editor
for creating your own steps.

%prep
%forgesetup

%patch 1 -p1 -b .preview
%patch 2 -p1 -b .ffmpeg-avcodec
%patch 3 -p1 -b .ffmpeg-asm
%patch 4 -p1 -b .ffmpeg-frame-num
%patch 5 -p1 -b .long-musicwheel

%build
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_libdir} \
    -DWITH_FULL_RELEASE=YES \
    -DWITH_PORTABLE_TOMCRYPT=NO \
    -DWITH_SYSTEM_FFMPEG=YES \
    -DWITH_SYSTEM_MAD=YES \
    -DWITH_SYSTEM_OGG=YES \
    -DWITH_SYSTEM_JPEG=YES \
    -DWITH_SYSTEM_PNG=YES \
    -DWITH_SYSTEM_GLEW=YES \
    -DWITH_SYSTEM_TOMMATH=YES \
    -DWITH_SYSTEM_TOMCRYPT=YES \
    -DWITH_SYSTEM_JSONCPP=YES \
    -DWITH_SYSTEM_PCRE=YES \
    -DWITH_SYSTEM_ZLIB=YES \
    -Wno-dev

%cmake_build

%install
%cmake_install

desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications stepmania.desktop

cp -R icons %{buildroot}/%{_datadir}/

mkdir -p %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{the_data_directory}/Docs/Licenses.txt %{buildroot}%{_docdir}/%{name}/
mv %{buildroot}%{the_data_directory}/Docs %{buildroot}%{_docdir}/%{name}/Docs

mkdir -p %{buildroot}%{_bindir}
cat <<EOF > %{buildroot}%{_bindir}/stepmania
#!/bin/sh
exec %{the_data_directory}/stepmania "\$@"
EOF

%check

%files
%{_bindir}/stepmania
%{the_data_directory}
%{_datadir}/icons/*/*/*/*.*
%{_datadir}/applications/stepmania.desktop
%license %{_docdir}/%{name}/Licenses.txt
%doc %{_docdir}/%{name}/Docs

%changelog
* Wed Jul 16 2025 Jan "Yenya" Kasprzak <kas@yenya.net> - 5.1.0~20250110gitd55acb1-5
- Mark main license file with %%license tag
- Move docs into %%{_docdir}
- Remove %%attr tags
- Add ExcludeArch for ppc64le

* Thu Mar 20 2025 Jan "Yenya" Kasprzak <kas@yenya.net> - 5.1.0~20250110gitd55acb1-4
- Pre-release style version tag

* Thu Jan 09 2025 Jan "Yenya" Kasprzak <kas@yenya.net> - 5.1.beta-3.20250110gitd55acb1
- Build against ffmpeg instead of ffmpeg-free

* Thu Jan 09 2025 Jan "Yenya" Kasprzak <kas@yenya.net> - 5.1.beta-2.20250110gitd55acb1
- Updated according to the review (ffmpeg-free, license tag)

* Thu Jan 09 2025 Jan "Yenya" Kasprzak <kas@yenya.net> - 5.1.beta-1.20250110gitd55acb1
- Initial RPM release
