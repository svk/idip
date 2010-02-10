from idip import Board, Nation, Province

def createStandardBoard():
    board = Board()
    
    board.addNation( Nation( "France" ) )
    board.addNation( Nation( "England" ) )
    board.addNation( Nation( "Germany" ) )
    board.addNation( Nation( "Russia" ) )
    board.addNation( Nation( "Austria" ) )
    board.addNation( Nation( "Turkey" ) )
    board.addNation( Nation( "Italy" ) )

    provinces = [
            # Africa
        Province( "Naf", "North Africa" ).addCoast(),
        Province( "Tun", "Tunis" ).makeSupply().addCoast(),

            # Austria
        Province( "Boh", "Bohemia" ),
        Province( "Bud", "Budapest" ).makeSupply(),
        Province( "Gal", "Galicia" ),
        Province( "Tri", "Trieste" ).makeSupply().addCoast(),
        Province( "Tyr", "Tyrolia" ),
        Province( "Vie", "Vienna" ).makeSupply(),

            # Balkans
        Province( "Bul", "Bulgaria" ).addCoast("EC").addCoast("SC").makeSupply(),
        Province( "Gre", "Greece" ).addCoast().makeSupply(),
        Province( "Rum", "Rumania" ).addCoast().makeSupply(),
        Province( "Ser", "Serbia" ).makeSupply(),
        Province( "Alb", "Albania" ).addCoast(),

            # England
        Province( "Cly", "Clyde" ).addCoast(),
        Province( "Edi", "Edinburgh" ).addCoast().makeSupply(),
        Province( "Lvp", "Liverpool" ).addCoast().makeSupply(),
        Province( "Lon", "London" ).addCoast().makeSupply(),
        Province( "Wal", "Wales" ).addCoast(),
        Province( "Yor", "Yorkshire" ).addCoast(),

            # France
        Province( "Bre", "Brest" ).addCoast().makeSupply(),
        Province( "Bur", "Burgundy" ),
        Province( "Gas", "Gascony" ).addCoast(),
        Province( "Mar", "Marseilles" ).addCoast().makeSupply(),
        Province( "Par", "Paris" ).makeSupply(),
        Province( "Pic", "Picardy" ).addCoast(),

            # Germany
        Province( "Ber", "Berlin" ).addCoast().makeSupply(),
        Province( "Kie", "Kiel" ).addCoast().makeSupply(),
        Province( "Mun", "Munich" ).makeSupply(),
        Province( "Pru", "Prussia" ).addCoast(),
        Province( "Ruh", "Ruhr" ),
        Province( "Sil", "Silesia" ),

            # Iberia
        Province( "Spa", "Spain" ).addCoast("NC").addCoast("SC").makeSupply(),
        Province( "Por", "Portugal" ).addCoast().makeSupply(),
        
            # Italy
        Province( "Apu", "Apulia" ).addCoast(),
        Province( "Nap", "Naples" ).addCoast().makeSupply(),
        Province( "Pie", "Piedmont" ).addCoast(),
        Province( "Rom", "Rome" ).addCoast().makeSupply(),
        Province( "Tus", "Tuscany" ).addCoast(),
        Province( "Ven", "Venice" ).addCoast().makeSupply(),

            # Low Countries
        Province( "Bel", "Belgium" ).addCoast().makeSupply(),
        Province( "Hol", "Holland" ).addCoast().makeSupply(),
        
            # Russia
        Province( "Fin", "Finland" ).addCoast(),
        Province( "Lvn", "Livonia" ).addCoast(),
        Province( "Mos", "Moscow" ).makeSupply(),
        Province( "Sev", "Sevastopol" ).addCoast().makeSupply(),
        Province( "Stp", "St. Petersburg" ).addCoast("NC").addCoast("SC").makeSupply(),
        Province( "Ukr", "Ukraine" ),
        Province( "War", "Warsaw" ).makeSupply(),

            # Denmark
        Province( "Den", "Denmark" ).addCoast().makeSupply(),
        Province( "Nwy", "Norway" ).addCoast().makeSupply(),
        Province( "Swe", "Sweden" ).addCoast().makeSupply(),

            # Turkey
        Province( "Con", "Constantinople").addCoast().makeSupply(),
        Province( "Ank", "Ankara").addCoast().makeSupply(),
        Province( "Smy", "Smyrna").addCoast().makeSupply(),
        Province( "Arm", "Armenia" ).addCoast(),
        Province( "Syr", "Syria" ).addCoast(),

            # Atlantic
        Province( "ENG", "English Channel" ),
        Province( "HEL", "Helgoland Blight" ),
        Province( "IRI", "Irish Sea" ),
        Province( "MAO", "Mid-Atlantic Ocean" ),
        Province( "NAO", "North-Atlantic Ocean" ),
        Province( "NTH", "North Sea" ),
        Province( "SKA", "Skagerrak" ),
        Province( "NWG", "Norwegian Sea" ),
        Province( "BAR", "Barents Sea" ),

            # Baltic
        Province( "BAL", "Baltic Sea" ),
        Province( "BOT", "Gulf of Bothnia" ),

            # Mediterranean
        Province( "BLA", "Black Sea" ),
        Province( "AEG", "Aegean Sea" ),
        Province( "ADR", "Adriatic Sea" ),
        Province( "EAS", "Eastern Mediterranean Sea" ),
        Province( "LYO", "Gulf of Lyons" ),
        Province( "ION", "Ionian Sea" ),
        Province( "TYS", "Tyrrhenian Sea" ),
        Province( "WES", "Western Mediterranean Sea" ),
    ]
    for province in provinces:
        board.addProvince( province )

    board.provinces.Lvp.setUnit( board.nations.England, "army" )
    board.provinces.Edi.coast().setUnit( board.nations.England, "fleet" )
    board.provinces.Lon.coast().setUnit( board.nations.England, "fleet" )
    board.nations.England.addHome( board.provinces.Lvp )
    board.nations.England.addHome( board.provinces.Edi )
    board.nations.England.addHome( board.provinces.Lon )

    board.provinces.Par.setUnit( board.nations.France, "army" )
    board.provinces.Mar.setUnit( board.nations.France, "army" )
    board.provinces.Bre.coast().setUnit( board.nations.France, "fleet" )
    board.nations.France.addHome( board.provinces.Par )
    board.nations.France.addHome( board.provinces.Mar )
    board.nations.France.addHome( board.provinces.Bre )

    board.provinces.Mun.setUnit( board.nations.Germany, "army" )
    board.provinces.Ber.setUnit( board.nations.Germany, "army" )
    board.provinces.Kie.coast().setUnit( board.nations.Germany, "fleet" )
    board.nations.Germany.addHome( board.provinces.Mun )
    board.nations.Germany.addHome( board.provinces.Ber )
    board.nations.Germany.addHome( board.provinces.Kie )

    board.provinces.Ven.setUnit( board.nations.Italy, "army" )
    board.provinces.Rom.setUnit( board.nations.Italy, "army" )
    board.provinces.Nap.coast().setUnit( board.nations.Italy, "fleet" )
    board.nations.Italy.addHome( board.provinces.Ven )
    board.nations.Italy.addHome( board.provinces.Rom )
    board.nations.Italy.addHome( board.provinces.Nap )

    board.provinces.Vie.setUnit( board.nations.Austria, "army" )
    board.provinces.Bud.setUnit( board.nations.Austria, "army" )
    board.provinces.Tri.coast().setUnit( board.nations.Austria, "fleet" )
    board.nations.Austria.addHome( board.provinces.Vie )
    board.nations.Austria.addHome( board.provinces.Bud )
    board.nations.Austria.addHome( board.provinces.Tri )

    board.provinces.Con.setUnit( board.nations.Turkey, "army" )
    board.provinces.Smy.setUnit( board.nations.Turkey, "army" )
    board.provinces.Ank.coast().setUnit( board.nations.Turkey, "fleet" )
    board.nations.Turkey.addHome( board.provinces.Con )
    board.nations.Turkey.addHome( board.provinces.Smy )
    board.nations.Turkey.addHome( board.provinces.Ank )

    board.provinces.War.setUnit( board.nations.Russia, "army" )
    board.provinces.Mos.setUnit( board.nations.Russia, "army" )
    board.provinces.Sev.coast().setUnit( board.nations.Russia, "fleet" )
    board.provinces.Stp.coast("SC").setUnit( board.nations.Russia, "fleet" )
    board.nations.Russia.addHome( board.provinces.War )
    board.nations.Russia.addHome( board.provinces.Mos )
    board.nations.Russia.addHome( board.provinces.Sev )
    board.nations.Russia.addHome( board.provinces.Stp )

        # Turkey
    board.provinces.Ank.coast().link( board.provinces.Con.coast() )
    board.provinces.Con.coast().link( board.provinces.Smy.coast() )
    board.provinces.Ank.coast().link( board.provinces.BLA )
    board.provinces.Con.coast().link( board.provinces.BLA )
    board.provinces.Con.coast().link( board.provinces.AEG )
    board.provinces.Smy.coast().link( board.provinces.AEG )
    board.provinces.Smy.coast().link( board.provinces.EAS )
    board.provinces.Con.link( board.provinces.Ank )
    board.provinces.Con.link( board.provinces.Smy )
    board.provinces.Smy.link( board.provinces.Ank )
    board.provinces.Ank.link( board.provinces.Arm )
    board.provinces.Arm.link( board.provinces.Smy )
    board.provinces.Smy.link( board.provinces.Syr )
    board.provinces.Syr.link( board.provinces.Arm )
    board.provinces.Con.link( board.provinces.Bul )

        # Russia
    board.provinces.Stp.coast("NC").link( board.provinces.BAR )
    board.provinces.Stp.coast("SC").link( board.provinces.BOT )
    board.provinces.Lvn.coast().link( board.provinces.BOT )
    board.provinces.Lvn.coast().link( board.provinces.BAL )
    board.provinces.Sev.coast().link( board.provinces.BLA )
    board.provinces.Lvn.link( board.provinces.War )
    board.provinces.Lvn.link( board.provinces.Mos )
    board.provinces.Lvn.link( board.provinces.Stp )
    board.provinces.War.link( board.provinces.Ukr )
    board.provinces.War.link( board.provinces.Mos )
    board.provinces.Ukr.link( board.provinces.War )
    board.provinces.Ukr.link( board.provinces.Mos )
    board.provinces.Ukr.link( board.provinces.Sev )
    board.provinces.Sev.link( board.provinces.Mos )
    board.provinces.Sev.link( board.provinces.Ukr )
    board.provinces.Sev.link( board.provinces.Arm )


        # Coasts
    board.provinces.Stp.coast("NC").link( board.provinces.BAR )
    board.provinces.Stp.coast("NC").link( board.provinces.Nwy.coast() )
    board.provinces.Nwy.coast().link( board.provinces.BAR )
    board.provinces.Nwy.coast().link( board.provinces.NWG )
    board.provinces.Nwy.coast().link( board.provinces.NTH )
    board.provinces.Nwy.coast().link( board.provinces.SKA )
    board.provinces.Nwy.coast().link( board.provinces.Swe.coast() )
    board.provinces.Swe.coast().link( board.provinces.SKA )
    board.provinces.Swe.coast().link( board.provinces.Den.coast() )
    board.provinces.Swe.coast().link( board.provinces.BAL )
    board.provinces.Swe.coast().link( board.provinces.BOT )
    board.provinces.Swe.coast().link( board.provinces.Fin.coast() )
    board.provinces.Fin.coast().link( board.provinces.BOT )
    board.provinces.Fin.coast().link( board.provinces.Stp.coast("SC") )
    board.provinces.Stp.coast("SC").link( board.provinces.BOT )
    board.provinces.Stp.coast("SC").link( board.provinces.Lvn.coast() )
    board.provinces.Lvn.coast().link( board.provinces.BOT )
    board.provinces.Lvn.coast().link( board.provinces.BAL )
    board.provinces.Lvn.coast().link( board.provinces.Pru.coast() )
    board.provinces.Pru.coast().link( board.provinces.BAL )
    board.provinces.Pru.coast().link( board.provinces.Ber.coast() )
    board.provinces.Ber.coast().link( board.provinces.BAL )
    board.provinces.Ber.coast().link( board.provinces.Kie.coast() )
    board.provinces.Kie.coast().link( board.provinces.BAL )
    board.provinces.Kie.coast().link( board.provinces.HEL )
    board.provinces.Kie.coast().link( board.provinces.Den.coast() )
    board.provinces.Den.coast().link( board.provinces.BAL )
    board.provinces.Den.coast().link( board.provinces.SKA )
    board.provinces.Den.coast().link( board.provinces.NTH )
    board.provinces.Den.coast().link( board.provinces.HEL )
    board.provinces.Den.coast().link( board.provinces.Kie.coast() )
    board.provinces.Kie.coast().link( board.provinces.Hol.coast() )
    board.provinces.Hol.coast().link( board.provinces.NTH )
    board.provinces.Hol.coast().link( board.provinces.HEL )
    board.provinces.Hol.coast().link( board.provinces.Bel.coast() )
    board.provinces.Bel.coast().link( board.provinces.NTH )
    board.provinces.Bel.coast().link( board.provinces.ENG )
    board.provinces.Bel.coast().link( board.provinces.Pic.coast() )
    board.provinces.Pic.coast().link( board.provinces.ENG )
    board.provinces.Pic.coast().link( board.provinces.Bre.coast() )
    board.provinces.Bre.coast().link( board.provinces.ENG )
    board.provinces.Bre.coast().link( board.provinces.MAO )
    board.provinces.Bre.coast().link( board.provinces.Gas.coast() )
    board.provinces.Gas.coast().link( board.provinces.MAO )
    board.provinces.Gas.coast().link( board.provinces.Spa.coast("NC") )
    board.provinces.Spa.coast("NC").link( board.provinces.MAO )
    board.provinces.Spa.coast("NC").link( board.provinces.Por )
    board.provinces.Por.coast().link( board.provinces.MAO )
    board.provinces.Por.coast().link( board.provinces.Spa.coast("SC") )
    board.provinces.Spa.coast("SC").link( board.provinces.MAO )
    board.provinces.Spa.coast("SC").link( board.provinces.WES )
    board.provinces.Spa.coast("SC").link( board.provinces.LYO )
    board.provinces.Spa.coast("SC").link( board.provinces.Mar.coast() )
    board.provinces.Mar.coast().link( board.provinces.LYO )
    board.provinces.Mar.coast().link( board.provinces.Pie.coast() )
    board.provinces.Pie.coast().link( board.provinces.LYO )
    board.provinces.Pie.coast().link( board.provinces.Tus.coast() )
    board.provinces.Tus.coast().link( board.provinces.LYO )
    board.provinces.Tus.coast().link( board.provinces.TYS )
    board.provinces.Tus.coast().link( board.provinces.Rom.coast() )
    board.provinces.Rom.coast().link( board.provinces.TYS )
    board.provinces.Rom.coast().link( board.provinces.Nap.coast() )
    board.provinces.Nap.coast().link( board.provinces.TYS )
    board.provinces.Nap.coast().link( board.provinces.ION )
    board.provinces.Nap.coast().link( board.provinces.Apu.coast() )
    board.provinces.Apu.coast().link( board.provinces.ION )
    board.provinces.Apu.coast().link( board.provinces.ADR )
    board.provinces.Apu.coast().link( board.provinces.Ven.coast() )
    board.provinces.Ven.coast().link( board.provinces.ADR )
    board.provinces.Ven.coast().link( board.provinces.Tri.coast() )
    board.provinces.Tri.coast().link( board.provinces.ADR )
    board.provinces.Tri.coast().link( board.provinces.Alb.coast() )
    board.provinces.Alb.coast().link( board.provinces.ADR )
    board.provinces.Alb.coast().link( board.provinces.ION )
    board.provinces.Alb.coast().link( board.provinces.Gre.coast() )
    board.provinces.Gre.coast().link( board.provinces.ION )
    board.provinces.Gre.coast().link( board.provinces.AEG )
    board.provinces.Gre.coast().link( board.provinces.Bul.coast("SC") )
    board.provinces.Bul.coast("SC").link( board.provinces.AEG )
    board.provinces.Bul.coast("SC").link( board.provinces.Con.coast() )
    board.provinces.Con.coast().link( board.provinces.AEG )
    board.provinces.Con.coast().link( board.provinces.Bul.coast("EC") )
    board.provinces.Con.coast().link( board.provinces.BLA )
    board.provinces.Bul.coast("EC").link( board.provinces.BLA )
    board.provinces.Bul.coast("EC").link( board.provinces.Rum.coast() )
    board.provinces.Rum.coast().link( board.provinces.BLA )
    board.provinces.Rum.coast().link( board.provinces.Sev.coast() )
    board.provinces.Sev.coast().link( board.provinces.BLA )
    board.provinces.Sev.coast().link( board.provinces.Arm.coast() )
    board.provinces.Arm.coast().link( board.provinces.BLA )
    board.provinces.Arm.coast().link( board.provinces.Ank.coast() )
    board.provinces.Ank.coast().link( board.provinces.BLA )
    board.provinces.Ank.coast().link( board.provinces.Con.coast() )
    board.provinces.Con.coast().link( board.provinces.Smy.coast() )
    board.provinces.Smy.coast().link( board.provinces.AEG )
    board.provinces.Smy.coast().link( board.provinces.EAS )
    board.provinces.Smy.coast().link( board.provinces.Syr.coast() )
    board.provinces.Syr.coast().link( board.provinces.EAS )

    board.provinces.Naf.coast().link( board.provinces.MAO )
    board.provinces.Naf.coast().link( board.provinces.WES )
    board.provinces.Naf.coast().link( board.provinces.Tun.coast() )
    board.provinces.Tun.coast().link( board.provinces.WES )
    board.provinces.Tun.coast().link( board.provinces.TYS )
    board.provinces.Tun.coast().link( board.provinces.ION )

    board.provinces.Cly.coast().link( board.provinces.NWG )
    board.provinces.Cly.coast().link( board.provinces.NAO )
    board.provinces.Cly.coast().link( board.provinces.Lvp.coast() )
    board.provinces.Lvp.coast().link( board.provinces.NAO )
    board.provinces.Lvp.coast().link( board.provinces.IRI )
    board.provinces.Lvp.coast().link( board.provinces.Wal.coast() )
    board.provinces.Wal.coast().link( board.provinces.IRI )
    board.provinces.Wal.coast().link( board.provinces.ENG )
    board.provinces.Wal.coast().link( board.provinces.Lon.coast() )
    board.provinces.Lon.coast().link( board.provinces.ENG )
    board.provinces.Lon.coast().link( board.provinces.NTH )
    board.provinces.Lon.coast().link( board.provinces.Yor.coast() )
    board.provinces.Yor.coast().link( board.provinces.NTH )
    board.provinces.Yor.coast().link( board.provinces.Edi.coast() )
    board.provinces.Edi.coast().link( board.provinces.NTH )
    board.provinces.Edi.coast().link( board.provinces.NWG )
    board.provinces.Edi.coast().link( board.provinces.Cly.coast() )

        # Ocean links
    board.provinces.BAR.linkMultiple( [ board.provinces.NWG ] )
    board.provinces.NWG.linkMultiple( [ board.provinces.BAR,
                                 board.provinces.NAO,
                                 board.provinces.NTH ] )
    board.provinces.NAO.linkMultiple( [ board.provinces.NWG,
                                 board.provinces.IRI,
                                 board.provinces.MAO ] )
    board.provinces.NTH.linkMultiple( [ board.provinces.NWG,
                                 board.provinces.SKA,
                                 board.provinces.HEL,
                                 board.provinces.ENG ] )
    board.provinces.SKA.linkMultiple( [ board.provinces.NTH ] )
    board.provinces.BAL.linkMultiple( [ board.provinces.BOT ] )
    board.provinces.BOT.linkMultiple( [ board.provinces.BAL ] )
    board.provinces.HEL.linkMultiple( [ board.provinces.NTH ] )
    board.provinces.IRI.linkMultiple( [ board.provinces.NAO,
                                 board.provinces.MAO,
                                 board.provinces.ENG ] )
    board.provinces.MAO.linkMultiple( [ board.provinces.NAO,
                                 board.provinces.IRI,
                                 board.provinces.ENG,
                                 board.provinces.WES ] )
    board.provinces.WES.linkMultiple( [ board.provinces.MAO,
                                 board.provinces.LYO,
                                 board.provinces.TYS ] )
    board.provinces.LYO.linkMultiple( [ board.provinces.WES,
                                 board.provinces.TYS ] )
    board.provinces.TYS.linkMultiple( [ board.provinces.WES,
                                 board.provinces.LYO,
                                 board.provinces.ION ] )
    board.provinces.ION.linkMultiple( [ board.provinces.TYS,
                                 board.provinces.ADR,
                                 board.provinces.AEG,
                                 board.provinces.EAS ] )
    board.provinces.ADR.linkMultiple( [ board.provinces.ION ] )
    board.provinces.AEG.linkMultiple( [ board.provinces.ION,
                                 board.provinces.EAS ] )
    board.provinces.EAS.linkMultiple( [ board.provinces.ION,
                                 board.provinces.AEG ] )
    board.provinces.BLA.linkMultiple( [] )

    board.provinces.Nwy.linkMultiple( [
        board.provinces.Swe,
        board.provinces.Fin,
        board.provinces.Stp,
    ] )
    board.provinces.Swe.linkMultiple( [
        board.provinces.Nwy,
        board.provinces.Den,
        board.provinces.Fin,
    ] )
    board.provinces.Fin.linkMultiple( [
        board.provinces.Nwy,
        board.provinces.Swe,
        board.provinces.Stp,
    ] )
    board.provinces.Stp.linkMultiple( [
        board.provinces.Nwy,
        board.provinces.Fin,
        board.provinces.Lvn,
        board.provinces.Mos,
    ] )
    board.provinces.Lvn.linkMultiple( [
        board.provinces.Pru,
        board.provinces.War,
        board.provinces.Mos,
        board.provinces.Stp,
    ] )
    board.provinces.Mos.linkMultiple( [
        board.provinces.Stp,
        board.provinces.Lvn,
        board.provinces.War,
        board.provinces.Ukr,
        board.provinces.Sev,
    ] )
    board.provinces.Sev.linkMultiple( [
        board.provinces.Mos,
        board.provinces.Ukr,
        board.provinces.Rum,
        board.provinces.Arm,
    ] )
    board.provinces.Arm.linkMultiple( [
        board.provinces.Sev,
        board.provinces.Ank,
        board.provinces.Smy,
        board.provinces.Syr,
    ] )
    board.provinces.Ank.linkMultiple( [
        board.provinces.Con,
        board.provinces.Smy,
        board.provinces.Arm,
    ] )
    board.provinces.Smy.linkMultiple( [
        board.provinces.Con,
        board.provinces.Ank,
        board.provinces.Arm,
        board.provinces.Syr,
    ] )
    board.provinces.Syr.linkMultiple( [
        board.provinces.Arm,
        board.provinces.Smy,
    ] )
    board.provinces.Con.linkMultiple( [
        board.provinces.Bul,
        board.provinces.Smy,
        board.provinces.Ank,
    ] )
    board.provinces.Bul.linkMultiple( [
        board.provinces.Con,
        board.provinces.Gre,
        board.provinces.Ser,
        board.provinces.Rum,
    ] )
    board.provinces.Rum.linkMultiple( [
        board.provinces.Bul,
        board.provinces.Ser,
        board.provinces.Bud,
        board.provinces.Gal,
        board.provinces.Ukr,
        board.provinces.Sev,
    ] )
    board.provinces.Ukr.linkMultiple( [
        board.provinces.War,
        board.provinces.Mos,
        board.provinces.Sev,
        board.provinces.Rum,
        board.provinces.Gal,
    ] )
    board.provinces.Pru.linkMultiple( [
        board.provinces.Ber,
        board.provinces.Sil,
        board.provinces.War,
        board.provinces.Lvn,
    ] )
    board.provinces.War.linkMultiple( [
        board.provinces.Pru,
        board.provinces.Sil,
        board.provinces.Gal,
        board.provinces.Ukr,
        board.provinces.Mos,
        board.provinces.Lvn,
    ] )
    board.provinces.Gal.linkMultiple( [
        board.provinces.Sil,
        board.provinces.Boh,
        board.provinces.Vie,
        board.provinces.Bud,
        board.provinces.Rum,
        board.provinces.Ukr,
        board.provinces.War,
    ] )
    board.provinces.Bud.linkMultiple( [
        board.provinces.Gal,
        board.provinces.Vie,
        board.provinces.Tri,
        board.provinces.Ser,
        board.provinces.Rum,
    ] )
    board.provinces.Ser.linkMultiple( [
        board.provinces.Bud,
        board.provinces.Tri,
        board.provinces.Alb,
        board.provinces.Gre,
        board.provinces.Bul,
        board.provinces.Rum,
    ] )
    board.provinces.Alb.linkMultiple( [
        board.provinces.Tri,
        board.provinces.Ser,
        board.provinces.Gre,
    ] )
    board.provinces.Gre.linkMultiple( [
        board.provinces.Alb,
        board.provinces.Ser,
        board.provinces.Bul,
    ] )
    board.provinces.Sil.linkMultiple( [
        board.provinces.Pru,
        board.provinces.Ber,
        board.provinces.Mun,
        board.provinces.Boh,
        board.provinces.Gal,
        board.provinces.War,
    ] )
    board.provinces.Boh.linkMultiple( [
        board.provinces.Sil,
        board.provinces.Mun,
        board.provinces.Tyr,
        board.provinces.Vie,
        board.provinces.Gal,
    ] )
    board.provinces.Vie.linkMultiple( [
        board.provinces.Boh,
        board.provinces.Tyr,
        board.provinces.Tri,
        board.provinces.Bud,
        board.provinces.Gal,
    ] )
    board.provinces.Tri.linkMultiple( [
        board.provinces.Alb,
        board.provinces.Ser,
        board.provinces.Bud,
        board.provinces.Vie,
        board.provinces.Tyr,
        board.provinces.Ven,
    ] )
    board.provinces.Ber.linkMultiple( [
        board.provinces.Kie,
        board.provinces.Mun,
        board.provinces.Sil,
        board.provinces.Pru,
    ] )
    board.provinces.Kie.linkMultiple( [
        board.provinces.Ber,
        board.provinces.Mun,
        board.provinces.Ruh,
        board.provinces.Hol,
        board.provinces.Den,
    ] )
    board.provinces.Den.linkMultiple( [
        board.provinces.Kie,
        board.provinces.Swe,
    ] )
    board.provinces.Hol.linkMultiple( [
        board.provinces.Bel,
        board.provinces.Ruh,
        board.provinces.Kie,
    ] )
    board.provinces.Ruh.linkMultiple( [
        board.provinces.Bel,
        board.provinces.Hol,
        board.provinces.Kie,
        board.provinces.Mun,
        board.provinces.Bur,
    ] )
    board.provinces.Bel.linkMultiple( [
        board.provinces.Pic,
        board.provinces.Bur,
        board.provinces.Ruh,
        board.provinces.Hol,
    ] )
    board.provinces.Tyr.linkMultiple( [
        board.provinces.Boh,
        board.provinces.Mun,
        board.provinces.Vie,
        board.provinces.Tri,
        board.provinces.Ven,
        board.provinces.Pie,
    ] )
    board.provinces.Pie.linkMultiple( [
        board.provinces.Mar,
        board.provinces.Tyr,
        board.provinces.Ven,
        board.provinces.Tus,
    ] )
    board.provinces.Tus.linkMultiple( [
        board.provinces.Pie,
        board.provinces.Ven,
        board.provinces.Rom,
    ] )
    board.provinces.Ven.linkMultiple( [
        board.provinces.Tyr,
        board.provinces.Tri,
        board.provinces.Pie,
        board.provinces.Tus,
        board.provinces.Rom,
        board.provinces.Apu,
    ] )
    board.provinces.Rom.linkMultiple( [
        board.provinces.Tus,
        board.provinces.Ven,
        board.provinces.Apu,
        board.provinces.Nap,
    ] )
    board.provinces.Apu.linkMultiple( [
        board.provinces.Ven,
        board.provinces.Rom,
        board.provinces.Nap,
    ] )
    board.provinces.Nap.linkMultiple( [
        board.provinces.Rom,
        board.provinces.Apu,
    ] )
    board.provinces.Pic.linkMultiple( [
        board.provinces.Bel,
        board.provinces.Bur,
        board.provinces.Par,
        board.provinces.Bre,
    ] )
    board.provinces.Bur.linkMultiple( [
        board.provinces.Pic,
        board.provinces.Par,
        board.provinces.Gas,
        board.provinces.Mar,
        board.provinces.Mun,
        board.provinces.Ruh,
        board.provinces.Bel,
    ] )
    board.provinces.Mar.linkMultiple( [
        board.provinces.Spa,
        board.provinces.Gas,
        board.provinces.Bur,
        board.provinces.Pie,
    ] )
    board.provinces.Spa.linkMultiple( [
        board.provinces.Por,
        board.provinces.Gas,
        board.provinces.Mar,
    ] )
    board.provinces.Por.linkMultiple( [
        board.provinces.Spa,
    ] )
    board.provinces.Gas.linkMultiple( [
        board.provinces.Spa,
        board.provinces.Mar,
        board.provinces.Bur,
        board.provinces.Par,
        board.provinces.Bre,
    ] )
    board.provinces.Bre.linkMultiple( [
        board.provinces.Pic,
        board.provinces.Par,
        board.provinces.Gas,
    ] )

    board.provinces.Naf.linkMultiple( [
        board.provinces.Tun,
    ] )
    board.provinces.Tun.linkMultiple( [
        board.provinces.Naf,
    ] )

    board.provinces.Wal.linkMultiple( [
        board.provinces.Lon,
        board.provinces.Yor,
        board.provinces.Lvp,
    ] )
    board.provinces.Lvp.linkMultiple( [
        board.provinces.Wal,
        board.provinces.Yor,
        board.provinces.Edi,
        board.provinces.Cly,
    ] )
    board.provinces.Lon.linkMultiple( [
        board.provinces.Wal,
        board.provinces.Yor,
    ] )
    board.provinces.Yor.linkMultiple( [
        board.provinces.Lon,
        board.provinces.Wal,
        board.provinces.Lvp,
        board.provinces.Edi,
    ] )
    board.provinces.Edi.linkMultiple( [
        board.provinces.Cly,
        board.provinces.Lvp,
        board.provinces.Yor,
    ] )
    board.provinces.Cly.linkMultiple( [
        board.provinces.Edi,
        board.provinces.Lvp,
    ] )

    return board

if __name__ == '__main__':
    board = createStandardBoard()
    for line in board.exportState():
        print( line )
