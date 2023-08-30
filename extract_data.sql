-- script to extract full specimen data from mysql
-- note this includes only current IDs

SELECT
	s.barcode, s.accession, s.id as specid, cl.exherb, cl.exno, colls.namestring as collectors, c.prefix as prefix, c.number, tc.typecat, typesp.fullname as typeof, cl.faa,
	dh.curdet, dh.family, dh.genus, dh.herbcode, 
	dh.sp1, dh.author1, dh.rank1, dh.sp2, dh.author2, dh.rank2, dh.sp3, dh.author3, dh.fullname, 
    dh.detby, dh.detday, dh.detmonth, dh.detyear, dh.detstatus, 
    co.continent, co.region, co.coname as country, g.major, g.minor, g.locality as gazlocality, c.locnotes, g.lat as gazlat, g.ns as gazns, g.long as gazlong, g.ew as gazew, g.alt1 as gazalt1, g.alt2 as gazalt2,
    g.llres as gazllres, g.llunit as gazllunit, g.qds as gazqds, g.gaznotes, 
    c.lat as speclat, c.ns as specns, c.long as speclong, c.ew as specew, c.llres as specllres, c.qds as specqds, c.alt1 as specalt, c.habitattxt, 
    cl.locvegtype as vegtype, cl.lochabitat as habitat, cl.locsubstra as substrate, cl.locmoistur as moisture, cl.locsoil as soil, cl.loclitholo as lithology, cl.locexposur as exposure, cl.locaspect as aspect, cl.bioticeffe as bioticeffect, 
    c.day as collday, c.month as collmonth, c.year as collyear, c.datetext as datetext,
    cl.flcode, cl.frcode, c.plantdesc, c.notes, c.initial, c.available
from specimens s
left outer join species as typesp on s.sptype = typesp.spnumber -- not every specimen has a typesp record, only some of the types
left outer join collections c on s.brahms = c.brahms -- every specimen has a collection record
left outer join peopleview colls on c.pview = colls.id
left outer join botrecordcats brc on c.category = brc.abbreviate
left outer join colllink cl on cl.brahms = c.brahms
left outer join gaz g on c.gazcode = g.gazcode
left outer join country co on g.conumber = co.conumber
left outer join ih on s.hbcode = ih.id
left outer join typecategories tc on s.hstype = tc.id
left outer join (
	select
		dh.specid, dh.curdet, f.faname as family, ge.gename as genus, ge.herbcode, 
		sp.sp1, au1.namestring as author1, sp.rank1, sp.sp2, au2.namestring as author2, sp.rank2, sp.sp3, au3.namestring as author3, sp.fullname as fullname,
		detby.namestring as detby, dh.detday, dh.detmonth, dh.detyear, dh.detstatus
	from dethistory dh -- on s.id = dh.specid
	left outer join peopleview detby on dh.detbyid = detby.id
	left outer join species sp on dh.spnumber = sp.spnumber
	left outer join peopleview au1 on sp.aucode1 = au1.id
	left outer join peopleview au2 on sp.aucode2 = au2.id
	left outer join peopleview au3 on sp.aucode3 = au3.id
	left outer join genus ge on sp.gecode = ge.gecode
	left outer join peopleview gau on ge.aucode = gau.id
	left outer join family f on ge.facode = f.facode
	where dh.curdet is not null and trim(dh.curdet) != ''
) as dh on s.id = dh.specid
