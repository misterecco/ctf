 2f0:	44 8b 07             	mov    r8d,DWORD PTR [rdi]
 2f3:	8b 47 10             	mov    eax,DWORD PTR [rdi+0x10]
 2f6:	45 89 c1             	mov    r9d,r8d
 2f9:	41 f7 d1             	not    r9d
 2fc:	44 89 c9             	mov    ecx,r9d
 2ff:	21 f1                	and    ecx,esi
 301:	31 c8                	xor    eax,ecx
 303:	0f af 47 0c          	imul   eax,DWORD PTR [rdi+0xc]
 307:	89 c2                	mov    edx,eax
 309:	8b 47 08             	mov    eax,DWORD PTR [rdi+0x8]
 30c:	31 c8                	xor    eax,ecx
 30e:	0f af 47 04          	imul   eax,DWORD PTR [rdi+0x4]
 312:	01 d0                	add    eax,edx
 314:	8b 57 1c             	mov    edx,DWORD PTR [rdi+0x1c]
 317:	01 c8                	add    eax,ecx
 319:	8b 4f 20             	mov    ecx,DWORD PTR [rdi+0x20]
 31c:	44 21 c0             	and    eax,r8d
 31f:	31 c6                	xor    esi,eax
 321:	41 21 f0             	and    r8d,esi
 324:	44 31 c2             	xor    edx,r8d
 327:	0f af ca             	imul   ecx,edx
 32a:	8b 57 14             	mov    edx,DWORD PTR [rdi+0x14]
 32d:	44 31 c2             	xor    edx,r8d
 330:	0f af 57 18          	imul   edx,DWORD PTR [rdi+0x18]
 334:	01 ca                	add    edx,ecx
 336:	42 8d 04 02          	lea    eax,[rdx+r8*1]
 33a:	44 21 c8             	and    eax,r9d
 33d:	31 f0                	xor    eax,esi
 33f:	c3                   	ret
