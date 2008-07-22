%define _provides_exceptions libcrypto.so.0.9.7\\|libssl.so.0.9.7\\|devel(libcrypto)\\|devel(libssl)\\|devel(/lib/libNoVersion)\\|devel(libcrypto)
%define _requires_exceptions libcrypto.so.0.9.7\\|libssl.so.0.9.7\\|devel(/lib/libNoVersion)\\|devel(libcrypto)

%define maj 0.9.7
%define libname uClibc-libopenssl%maj
%define libnamedev %libname-devel
%define libnamestatic %libname-static-devel

%define basedir %{_prefix}/%{_target_cpu}-linux-uclibc
%define _mandir %{basedir}/usr/share/man
%define _bindir %{basedir}/usr/bin
%define _libdir %{basedir}/usr/lib
%define _docdir %{basedir}/usr/share/doc
%define _includedir %{basedir}/usr/include


# French policy is to not use ciphers stronger than 128 bits
%define french_policy 0

Summary:	Secure Sockets Layer communications libs & utils
Name:		uClibc-openssl
Version: 	0.9.7g
Release:	%mkrel 7
License:	BSD-like
Group:		System/Libraries
URL:		http://www.openssl.org/
Source:		ftp://ftp.openssl.org/source/openssl-%{version}.tar.bz2
# (gb) 0.9.6b-5mdk: Limit available SSL ciphers to 128 bits
Patch0:		openssl-0.9.6b-mdkconfig.patch
# (fg) 20010202 Patch from RH: some funcs now implemented with ia64 asm
Patch1:		openssl-0.9.7-ia64-asm.patch
# (gb) 0.9.7b-4mdk: Handle RPM_OPT_FLAGS in Configure
Patch2:		openssl-0.9.7g-optflags.diff
# (gb) 0.9.7b-4mdk: Make it lib64 aware. TODO: detect in Configure
Patch3:		openssl-0.9.7e-lib64.diff
# (oe) support Brazilian Government OTHERNAME X509v3 field (#14158)
# http://www.iti.gov.br/resolucoes/RESOLU__O_13_DE_26_04_2002.PDF
Patch6:		openssl-0.9.7-icpbrasil.diff
Patch7:		openssl-0.9.7-CAN-2005-2969.patch
Patch8:		openssl-0.9.7-CAN-2005-2946.patch
Patch9:		openssl-CVE-2006-4339.patch
Patch10:	openssl-0.9.7-CVE-2006-2940.patch
Patch11:	openssl-CVE-2006-4343.patch
Patch12:	openssl-0.9.7g-CVE-2006-3738.patch
Patch13:	openssl-0.9.7g-CVE-2006-2937.patch
Patch14:	openssl-0.9.7g-CVE-2006-2940-2.patch
Requires:	%libname = %version-%release
Requires:	perl-base
BuildRequires:	uClibc uClibc-devel uClibc-static-devel
BuildRoot:	%_tmppath/%name-%version-root

%description
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.
This product includes software developed by the OpenSSL Project for use in the
OpenSSL Toolkit (http://www.openssl.org/).
This product includes cryptographic software written by Eric Young
(eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).

%package -n %libnamedev
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	uClibc-libopenssl-devel uClibc-openssl-devel = %{version}-%{release}
Requires:	uClibc-devel uClibc-static-devel

%description -n %libnamedev
The static libraries and include files needed to compile apps with support
for various cryptographic algorithms and protocols, including DES, RC4, RSA
and SSL.
This product includes software developed by the OpenSSL Project for use in
the OpenSSL Toolkit (http://www.openssl.org/).
This product includes cryptographic software written by Eric Young
(eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).
Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%package -n %libnamestatic
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%libnamedev = %{version}-%{release}
Provides:	uClibc-libopenssl-static-devel uClibc-openssl-static-devel = %{version}-%{release}
Requires:	uClibc-devel uClibc-static-devel

%description -n %libnamestatic
The static libraries and include files needed to compile apps with support
for various cryptographic algorithms and protocols, including DES, RC4, RSA
and SSL.
This product includes software developed by the OpenSSL Project for use in
the OpenSSL Toolkit (http://www.openssl.org/).
This product includes cryptographic software written by Eric Young
(eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).
Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%package -n %{libname}
Summary:	Secure Sockets Layer communications libs
Group:		System/Libraries
Requires:	uClibc

%description -n %{libname}
The libraries files are needed for various cryptographic algorithms
and protocols, including DES, RC4, RSA and SSL.
This product includes software developed by the OpenSSL Project for use in
the OpenSSL Toolkit (http://www.openssl.org/).
This product includes cryptographic software written by Eric Young
(eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).
Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/

%prep

%setup -q -n openssl-%{version}
%if %{french_policy}
%patch0 -p1 -b .frenchpolicy
%endif
%patch1 -p1 -b .ia64-asm
%patch2 -p0 -b .optflags
%patch3 -p0 -b .lib64
%patch6 -p1 -b .icpbrasil
%patch7 -p1 -b .can-2005-2969
%patch8 -p1 -b .can-2005-2946
%patch9 -p0 -b .cve-2006-4339
%patch10 -p0 -b .cve-2006-2940
%patch11 -p0 -b .cve-2006-4343
%patch12 -p1 -b .cve-2006-3738
%patch13 -p1 -b .cve-2006-2937
%patch14 -p1 -b .cve-2006-2940-2

#perl -pi -e "s,^(LIB=).+$,\1%{_lib}," Makefile.org

%build 
# Don't carry out asm optimization on Alpha for now
# [gb] likewise on amd64: seems broken and no time to review
# [stefan@eijk.nu] ditto for sparc / sparc64
%ifarch alpha amd64 sparc sparc64 x86_64
NO_ASM="no-asm"
%endif
sh config $NO_ASM --prefix=%_prefix --openssldir=%_libdir/ssl shared
uclibc make
# All tests must pass
export LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
#uclibc make test

%install
rm -fr %{buildroot}
uclibc %makeinstall INSTALL_PREFIX=%{buildroot} MANDIR=%_mandir

pushd %{buildroot}/usr
mkdir -p %{buildroot}/%_includedir
mkdir -p %{buildroot}/%_libdir
mkdir -p %{buildroot}/%_bindir
mv bin/* %{buildroot}/%_bindir
mv include/* %{buildroot}/%_includedir
mv lib/* %{buildroot}/%_libdir
rmdir lib bin include
popd


cp -aRf *.so* %{buildroot}/%_libdir
cp -aRf *.a %{buildroot}/%_libdir

# openssl was named ssleay in "ancient" times.
ln -sf openssl %{buildroot}/%_bindir/ssleay

# The man pages rand.3 and passwd.1 conflict with other packages
# Rename them to ssl-* and also make a symlink from openssl-* to ssl-*
mv %{buildroot}/%_mandir/man1/passwd.1 %{buildroot}/%_mandir/man1/ssl-passwd.1
ln -sf ssl-passwd.1.bz2 %{buildroot}/%_mandir/man1/openssl-passwd.1.bz2

for i in rand err; do
mv %{buildroot}/%_mandir/man3/$i.3 %{buildroot}/%_mandir/man3/ssl-$i.3
ln -sf ssl-$i.3.bz2 %{buildroot}/%_mandir/man3/openssl-$i.3.bz2
done

rm -rf {main,devel}-doc-info
mkdir -p {main,devel}-doc-info
cat - << EOF > main-doc-info/README.Mandrake-manpage
Warning:
The man page of passwd, passwd.1, has been renamed to ssl-passwd.1
to avoid a conflict with passwd.1 man page from the package passwd.
EOF

cat - << EOF > devel-doc-info/README.Mandrake-manpage
Warning:
The man page of rand, rand.3, has been renamed to ssl-rand.3
to avoid a conflict with rand.3 from the package man-pages
The man page of err, err.3, has been renamed to ssl-err.3
to avoid a conflict with err.3 from the package man-pages
EOF

rm -f %{buildroot}%{_libdir}/libssl.so.0
rm -f %{buildroot}%{_libdir}/libcrypto.so.0
cd %{buildroot}%{_libdir}
ln -sf libssl.so.0.* libssl.so
ln -sf libcrypto.so.0.* libcrypto.so

mkdir -p %{buildroot}%{basedir}/lib
pushd %{buildroot}%{basedir}/lib
    ln -sf ../usr/lib/*.so* .
popd

chmod 755 %{buildroot}%{_libdir}/pkgconfig

%clean
rm -fr %buildroot

%files 
%defattr(-,root,root)
%doc LICENSE CHANGES FAQ NEWS README
%doc main-doc-info/README*
%_bindir/*
%dir %_libdir/ssl
%_libdir/ssl/*
%_mandir/man[157]/*

%files -n %{libname}
%defattr(-,root,root)
%_libdir/lib*.so.*
%{basedir}/lib/lib*.so.*

%files -n %libnamedev
%defattr(-,root,root)
%doc doc/*
%doc devel-doc-info/README*
%dir %_includedir/openssl/
%_includedir/openssl/*
%_libdir/lib*.so
%{basedir}/lib/lib*.so
%_mandir/man3/*
%_libdir/pkgconfig/*

%files -n %libnamestatic
%defattr(-,root,root)
%_libdir/lib*.a

%post -n %{libname} -p %{basedir}/sbin/ldconfig

%postun -n %{libname} -p %{basedir}/sbin/ldconfig


