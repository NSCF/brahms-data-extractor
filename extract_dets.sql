select
		dh.specid, dh.curdet, f.faname as family, ge.gename as genus, ge.herbcode, 
		sp.sp1, au1.namestring as author1, sp.rank1, sp.sp2, au2.namestring as author2, sp.rank2, sp.sp3, au3.namestring as author3, sp.fullname as fullname,
		detby.namestring as detby, dh.detday, dh.detmonth, dh.detyear, dh.detstatus, dh.detnotes
	from dethistory dh -- on s.id = dh.specid
	left outer join peopleview detby on dh.detbyid = detby.id
	left outer join species sp on dh.spnumber = sp.spnumber
	left outer join peopleview au1 on sp.aucode1 = au1.id
	left outer join peopleview au2 on sp.aucode2 = au2.id
	left outer join peopleview au3 on sp.aucode3 = au3.id
	left outer join genus ge on sp.gecode = ge.gecode
	left outer join peopleview gau on ge.aucode = gau.id
	left outer join family f on ge.facode = f.facode
	where dh.curdet is null or trim(dh.curdet) = ''