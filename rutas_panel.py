"""Panel web interactivo Integra Life."""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Panel"])

PAGINA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integra Life</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
         background: #F4F6F9;
         min-height: 100vh; color: #363F4C; padding: 1.6rem; }
  header { display: flex; align-items: center; gap: .9rem; margin-bottom: 1.5rem;
           padding-bottom: 1rem; border-bottom: 3px solid #26529E; }
  .btn-menu { border: none; background: white; border: 1px solid #E3E7EE; border-radius: 3px;
              width: 44px; height: 44px; cursor: pointer; display: flex; flex-direction: column;
              align-items: center; justify-content: center; gap: 4px; flex-shrink: 0;
              transition: background .15s; }
  .btn-menu:hover { background: #F5F7FA; }
  .btn-menu span { display: block; width: 20px; height: 2px; background: #26529E;
                   transition: transform .3s, opacity .2s; }
  .btn-menu.abierto span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
  .btn-menu.abierto span:nth-child(2) { opacity: 0; }
  .btn-menu.abierto span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
  #velo-menu { position: fixed; inset: 0; background: rgba(54,63,76,.45); z-index: 70;
               opacity: 0; pointer-events: none; transition: opacity .28s ease; }
  #velo-menu.abierto { opacity: 1; pointer-events: auto; }
  .lateral { position: fixed; top: 0; left: 0; height: 100%; width: 268px; background: white;
             z-index: 80; box-shadow: 4px 0 24px rgba(54,63,76,.18);
             transform: translateX(-100%); transition: transform .32s cubic-bezier(.4,0,.2,1);
             display: flex; flex-direction: column; }
  .lateral.abierto { transform: translateX(0); }
  .lateral-cabecera { background: #26529E; color: white; padding: 1.4rem 1.3rem; }
  .lateral-cabecera .titulo { font-size: 1.15rem; font-weight: 700; letter-spacing: .02em; }
  .lateral-cabecera .sub2 { font-size: .78rem; opacity: .82; margin-top: .15rem; }
  .lateral-nav { padding: .8rem .7rem; flex: 1; overflow-y: auto; }
  .nav-item { display: flex; align-items: center; gap: .8rem; width: 100%; border: none;
              background: transparent; text-align: left; padding: .8rem .9rem; cursor: pointer;
              border-radius: 2px; font-size: .93rem; font-weight: 600; color: #363F4C;
              margin-bottom: .15rem; transition: background .15s, color .15s;
              border-left: 3px solid transparent; }
  .nav-item:hover { background: #F5F7FA; }
  .nav-item.activa { background: #E3EAF5; color: #26529E; border-left-color: #26529E; }
  .nav-item .ico { font-size: 1.05rem; width: 22px; text-align: center; }
  .lateral-pie { padding: .9rem 1.2rem; border-top: 1px solid #E3E7EE; font-size: .74rem;
                 color: #7B8494; }
  .titulo-vista { font-size: 1.15rem; font-weight: 700; color: #363F4C; }
  .cargando-voz { text-align: center; padding: 2.2rem 1rem; }
  .girador { width: 46px; height: 46px; margin: 0 auto 1.2rem;
             border: 4px solid #E3E7EE; border-top-color: #26529E;
             border-radius: 50%; animation: girar .9s linear infinite; }
  @keyframes girar { to { transform: rotate(360deg); } }
  .cargando-texto { font-size: 1rem; font-weight: 700; color: #26529E; }
  .cargando-sub { font-size: .82rem; color: #7B8494; margin-top: .35rem; }

  @media (max-width: 620px) {
    body { padding: .8rem; }
    .lateral { width: 84%; max-width: 300px; }
    .btn-flotante { right: .9rem; bottom: .9rem; width: 58px; height: 58px; font-size: 1.4rem; }

    header { gap: .6rem; padding-bottom: .7rem; margin-bottom: 1rem; }
    h1 { font-size: 1.05rem; }
    .sub { font-size: .72rem; }
    .logo { width: 38px; height: 38px; font-size: .95rem; }
    .btn-menu { width: 40px; height: 40px; }
    .btn-usuario { padding: .4rem .7rem; font-size: .78rem; max-width: 120px;
                   overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

    .barra { gap: .5rem; margin-bottom: .9rem; }
    .titulo-vista { font-size: 1rem; }
    .btn-nuevo { padding: .5rem .9rem; font-size: .82rem; }

    .grid { grid-template-columns: 1fr; gap: .7rem; }
    .tarjeta { padding: .9rem 1rem; }
    .tarjeta h3 { font-size: .96rem; }

    .barra-busqueda, #selector-org { flex-direction: column; align-items: stretch; }
    .filtro-org, .buscador { max-width: 100%; width: 100%; }
    .lbl-filtro { font-size: .7rem; }

    #velo { padding: 0; align-items: stretch; }
    .ficha { max-width: 100%; min-height: 100vh; border-radius: 0; border-top: none;
             padding: 1.1rem 1rem 4rem; }
    .ficha h2 { font-size: 1.08rem; }
    .cerrar { padding: .5rem .85rem; font-size: .82rem; }

    .dos-cols { grid-template-columns: 1fr; }
    .rev-campos { grid-template-columns: 1fr; }
    .ventanas { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .ventana-btn { padding: .55rem .7rem; font-size: .8rem; white-space: nowrap; }

    input[type=text], select, textarea { font-size: 16px; padding: .7rem .8rem; }
    .btn-guardar, .btn-nuevo, .btn-voz, .btn-brief { padding: .7rem 1.1rem; }

    .brief { padding: 1.1rem 1rem; }
    .brief h3 { font-size: 1.02rem; }
    .brief .resumen { font-size: .9rem; }
    .brief-cabecera { flex-direction: column; align-items: stretch; gap: .6rem; }
    .btn-brief { width: 100%; }

    .btn-grabar { width: 112px; height: 112px; font-size: .76rem; }
    .controles-voz { flex-wrap: wrap; justify-content: center; }
    .zona-voz, .zona-importar { padding: 1.1rem 1rem; }

    .hoy-evento { flex-direction: column; gap: .3rem; }
    .hoy-evento .hora-grande { min-width: 0; }
    .evento-acciones { opacity: 1; }
    .dato { flex-direction: column; align-items: flex-start; gap: .1rem; }
    .dato .valor { max-width: 100%; text-align: left; }
    .kpi-perfil { grid-template-columns: repeat(2, 1fr); }
    .contador-org { gap: .5rem; }
    .kpi { flex: 1; padding: .6rem .8rem; }
    .kpi .num { font-size: 1.15rem; }
    .tarea-persona { flex-wrap: wrap; }
  }
  .logo { width: 42px; height: 42px; border-radius: 3px;
          background: #26529E;
          display: flex; align-items: center; justify-content: center;
          color: white; font-weight: 800; font-size: 1.1rem;
          box-shadow: 0 2px 6px rgba(38,82,158,.18); }
  h1 { font-size: 1.3rem; color: #26529E; font-weight: 700; letter-spacing: .02em; }
  .sub { color: #7B8494; font-size: .85rem; margin-top: .1rem; }
.zona-usuario { margin-left: auto; display: flex; align-items: center; gap: .7rem; }
  .nombre-usuario { font-size: .85rem; color: #595959; font-weight: 600; }
  .btn-salir { border: none; border-radius: 3px; padding: .45rem 1rem; cursor: pointer; font-size: .85rem; font-weight: 700; color: #d84343; background: #fdeaea; }
  .btn-config { border: none; border-radius: 3px; padding: .45rem 1rem; cursor: pointer;
                font-size: .85rem; font-weight: 700; color: #26529E; background: #E3EAF5; }
  .btn-config:hover { background: #D3DDEC; }
  .menu-usuario { position: relative; }
  .btn-usuario { border: none; background: white; border-radius: 3px; cursor: pointer;
                 padding: .45rem 1rem; font-size: .85rem; font-weight: 700; color: #26529E;
                 box-shadow: 0 1px 2px rgba(54,63,76,.10); }
  .btn-usuario:hover { background: #F5F7FA; }
  .desplegable { position: absolute; right: 0; top: 110%; background: white;
                 border-radius: 3px; box-shadow: 0 1px 9px rgba(54,63,76,.10);
                 min-width: 190px; padding: .35rem; display: none; z-index: 60; }
  .desplegable.abierto { display: block; }
  .desplegable button { width: 100%; text-align: left; border: none; background: transparent;
                        padding: .6rem .8rem; border-radius: 3px; cursor: pointer;
                        font-size: .87rem; font-weight: 600; color: #363F4C; }
  .desplegable button:hover { background: #F5F7FA; }
  .desplegable button.rojo { color: #d84343; }
  .desplegable button.rojo:hover { background: #fdeaea; }
  .btn-flotante { position: fixed; right: 1.6rem; bottom: 1.6rem; width: 64px; height: 64px;
                  border-radius: 50%; border: none; cursor: pointer; z-index: 50;
                  background: #B03A3A; color: white;
                  font-size: 1.6rem; box-shadow: 0 3px 10px rgba(176,58,58,.28);
                  transition: transform .15s; }
  .btn-flotante:hover { transform: scale(1.07); }
  .btn-flotante.grabando { animation: latido 1.4s ease-in-out infinite; }
  .indicadores { display: flex; gap: .5rem; align-items: center; margin-top: .5rem;
                 font-size: .74rem; color: #7B8494; }
  .badge-pend { background: #fff5d9; color: #a37b12; font-weight: 800;
                border-radius: 3px; padding: .1rem .5rem; }
  .badge-pend.cero { background: #edf9f2; color: #17967c; }
  .filtro-org.activo { border-color: #2ec4a6; background: #f2fbf8; color: #17967c; }
  /* --- Vista Hoy --- */
  .hoy-seccion { grid-column: 1/-1; margin-top: .4rem; }
  .hoy-titulo { font-size: .8rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase;
                background: #26529E; padding: .45rem .9rem; border-radius: 2px;
                letter-spacing: .06em; margin-bottom: .7rem; display: flex; align-items: center; gap: .5rem; }
  .hoy-evento { background: white; border: 1px solid #E3E7EE; border-radius: 2px;
                padding: .9rem 1.1rem; margin-bottom: .6rem;
                box-shadow: 0 1px 3px rgba(54,63,76,.10); border-left: 5px solid #26529E;
                display: flex; gap: 1rem; align-items: flex-start; cursor: pointer; }
  .hoy-evento .hora-grande { font-size: 1.05rem; font-weight: 800; color: #26529E;
                             min-width: 62px; }
  .hoy-evento h4 { font-size: .98rem; margin-bottom: .15rem; }
  .hoy-pend { background: white; border-radius: 3px; padding: .65rem .9rem; margin-bottom: .5rem;
              box-shadow: 0 1px 2px rgba(54,63,76,.10); display: flex; gap: .7rem;
              align-items: center; cursor: pointer; border-left: 4px solid #e0a10b; }
  .hoy-pend:hover { background: #fffdf6; }
  .hoy-pend .quien { font-size: .74rem; color: #7B8494; font-weight: 700; }
  .hoy-pend .que { font-size: .88rem; }
  .hoy-frio { display: inline-flex; align-items: center; gap: .5rem; background: white;
              border-radius: 3px; padding: .4rem .9rem .4rem .4rem; margin: 0 .5rem .5rem 0;
              box-shadow: 0 1px 2px rgba(54,63,76,.10); cursor: pointer; font-size: .85rem; }
  .hoy-frio:hover { background: #F5F7FA; }
  .hoy-frio .avatar { width: 30px; height: 30px; font-size: .7rem; margin: 0; }
  .hoy-vacio { color: #A9B9D3; font-size: .85rem; font-style: italic; padding: .5rem 0 1rem; }
  .brief { grid-column: 1/-1; background: white; border: 1px solid #E3E7EE;
           border-top: 4px solid #26529E; border-radius: 3px; padding: 1.4rem 1.5rem;
           margin-bottom: 1rem; }
  .brief-cabecera { display: flex; justify-content: space-between; align-items: flex-start;
                    gap: 1rem; flex-wrap: wrap; margin-bottom: .8rem; }
  .brief-marca { font-size: .68rem; font-weight: 800; color: #26529E; letter-spacing: .1em;
                 text-transform: uppercase; margin-bottom: .3rem; }
  .brief h3 { font-size: 1.18rem; color: #363F4C; margin-bottom: .1rem; }
  .brief .resumen { font-size: .95rem; line-height: 1.6; color: #363F4C; margin: .9rem 0; }
  .brief-bloque { margin-top: 1.1rem; }
  .brief-bloque h5 { font-size: .72rem; font-weight: 800; text-transform: uppercase;
                     letter-spacing: .06em; color: #7B8494; margin-bottom: .5rem; }
  .brief-punto { display: flex; gap: .6rem; align-items: flex-start; font-size: .9rem;
                 line-height: 1.5; padding: .4rem 0; border-bottom: 1px solid #F0F2F6; }
  .brief-punto:last-child { border-bottom: none; }
  .brief-punto::before { content: "\25B8"; color: #26529E; font-weight: 800; flex-shrink: 0; }
  .btn-brief { border: none; background: #26529E; color: white; border-radius: 3px;
               padding: .5rem 1.1rem; cursor: pointer; font-size: .84rem; font-weight: 700;
               white-space: nowrap; }
  .btn-brief:hover { background: #1d4080; }
  .btn-brief:disabled { opacity: .55; cursor: wait; }
  .btn-brief.secundario { background: #E3EAF5; color: #26529E; }
  .btn-brief.secundario:hover { background: #D3DDEC; }
  .brief-pie { font-size: .72rem; color: #A9B9D3; margin-top: 1rem;
               border-top: 1px solid #F0F2F6; padding-top: .6rem; }
  .hoy-titulo.plegable { cursor: pointer; user-select: none; }
  .hoy-titulo.plegable:hover { color: #363F4C; }
  .flecha-pleg { transition: transform .2s; display: inline-block; font-size: .7rem; }
  .flecha-pleg.abierta { transform: rotate(90deg); }
  .conteo-pleg { background: #fff5d9; color: #a37b12; border-radius: 3px;
                 padding: .1rem .55rem; font-size: .72rem; font-weight: 800; }
  .conteo-pleg.cero { background: #edf9f2; color: #17967c; }
  #lista-pendientes { display: none; }
  #lista-pendientes.abierta { display: block; }
  .hoy-pend .detalle-pend { font-size: .76rem; color: #A9B9D3; margin-top: .25rem; }
  .btn-borrar-mini { border: none; background: transparent; cursor: pointer; color: #c9a0a0;
                     font-size: .95rem; padding: 0 .3rem; line-height: 1; }
  .btn-borrar-mini:hover { color: #d84343; }
  .evento { position: relative; }
  .evento-acciones { position: absolute; top: .8rem; right: .9rem; display: flex; gap: .35rem;
                     opacity: 0; transition: opacity .15s; }
  .evento:hover .evento-acciones { opacity: 1; }
  .btn-ev-accion { border: none; border-radius: 2px; padding: .25rem .55rem; cursor: pointer;
                   font-size: .78rem; font-weight: 700; }
  .btn-ev-accion.editar { background: #E3EAF5; color: #26529E; }
  .btn-ev-accion.borrar { background: #fdeaea; color: #d84343; }
  .chip-google { display: inline-block; font-size: .68rem; font-weight: 700; padding: .12rem .5rem;
                 border-radius: 3px; background: #EEEEEE; color: #595959; margin-left: .4rem; }
  .pendiente { position: relative; }
  .pendiente .borrar-tema { position: absolute; right: .5rem; top: 50%; transform: translateY(-50%);
                            opacity: 0; transition: opacity .15s; }
  .pendiente:hover .borrar-tema { opacity: 1; }
  .kpi-perfil { display: grid; grid-template-columns: repeat(4, 1fr); gap: .6rem; margin: 1rem 0; }
  .kpi-perfil .kpi { text-align: center; }
  .barra { display: flex; justify-content: space-between; align-items: center;
           margin-bottom: 1.3rem; flex-wrap: wrap; gap: .6rem; }
  .tabs { display: flex; gap: .5rem; flex-wrap: wrap; }
  .tab { padding: .55rem 1.2rem; border: none; border-radius: 3px; background: white;
         cursor: pointer; font-size: .9rem; font-weight: 600; color: #595959;
         box-shadow: 0 1px 2px rgba(54,63,76,.10); transition: all .15s; }
  .tab:hover { transform: translateY(-1px); }
  .tab.activa { background: #26529E; color: white; box-shadow: none;
                box-shadow: 0 2px 6px rgba(38,82,158,.18); }
  .btn-nuevo { border: none; border-radius: 3px; padding: .55rem 1.2rem; cursor: pointer;
               font-size: .9rem; font-weight: 700; color: white;
               background: #17967C;
               box-shadow: 0 2px 6px rgba(23,150,124,.18); transition: all .15s; }
  .btn-nuevo:hover { transform: translateY(-1px); }
  .btn-nuevo:disabled { opacity: .5; cursor: wait; }
  .barra-busqueda { margin-bottom: 1rem; }
  .buscador { width: 100%; max-width: 460px; border: 1px solid #D8DEE8; border-radius: 3px;
              padding: .68rem .9rem; font-size: .9rem; font-family: inherit; outline: none;
              background: white; color: #363F4C; box-shadow: 0 1px 2px rgba(54,63,76,.10); }
  .buscador:focus { border-color: #26529E; box-shadow: 0 0 0 3px rgba(91,108,255,.10); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 1rem; }
  .tarjeta { background: white; border: 1px solid #E3E7EE; border-radius: 3px; padding: 1.1rem 1.2rem;
             box-shadow: 0 1px 4px rgba(54,63,76,.10); cursor: pointer;
             transition: all .15s; border-top: 4px solid transparent; }
  .tarjeta:hover { transform: translateY(-3px); box-shadow: 0 2px 6px rgba(38,82,158,.18); }
  .tarjeta.cliente    { border-top-color: #26529E; }
  .tarjeta.proveedor  { border-top-color: #ff8a5b; }
  .tarjeta.socio      { border-top-color: #2ec4a6; }
  .tarjeta.empresario { border-top-color: #556D96; }
  .tarjeta.otro, .tarjeta.empresa { border-top-color: #A9B9D3; }
  .avatar { width: 40px; height: 40px; border-radius: 50%; display: inline-flex;
            align-items: center; justify-content: center; font-weight: 700;
            font-size: .9rem; color: white; margin-bottom: .55rem; }
  img.avatar { object-fit: cover; object-position: center; display: inline-block; background: #EEEEEE; }
  .avatar-grande { width: 76px; height: 76px; font-size: 1.15rem; margin-bottom: .35rem; }
  .foto-perfil { display: inline-flex; flex-direction: column; align-items: flex-start; gap: .2rem; margin-bottom: .35rem; }
  .btn-foto { border: none; background: transparent; color: #26529E; padding: .15rem 0; cursor: pointer;
              font-size: .74rem; font-weight: 700; font-family: inherit; }
  .btn-foto:hover { text-decoration: underline; }
  .tarjeta h3 { font-size: 1.02rem; margin-bottom: .15rem; }
  .meta { font-size: .8rem; color: #7B8494; }
  .chip { display: inline-block; margin-top: .55rem; margin-right: .3rem;
          padding: .18rem .65rem; border-radius: 3px; font-size: .72rem; font-weight: 700; }
  .chip.cliente    { background: #E3EAF5; color: #26529E; }
  .chip.proveedor  { background: #ffefe6; color: #d86a35; }
  .chip.socio      { background: #e2f7f2; color: #17967c; }
  .chip.empresario { background: #f1e8ff; color: #556D96; }
  .chip.otro       { background: #EEEEEE; color: #595959; }
  .chip.estado     { background: #fff5d9; color: #a37b12; }
  .selector-vista { display: flex; gap: .35rem; background: white; border-radius: 3px;
                    padding: .25rem; box-shadow: 0 1px 2px rgba(54,63,76,.10); }
  .vista-btn { border: none; background: transparent; border-radius: 3px;
               padding: .4rem .95rem; cursor: pointer; font-size: .82rem;
               font-weight: 700; color: #7B8494; transition: all .15s; white-space: nowrap; }
  .vista-btn:hover { color: #363F4C; }
  .vista-btn.activa { background: #17967C; color: white; }
  .lbl-filtro { font-size: .78rem; font-weight: 700; color: #7B8494;
                text-transform: uppercase; letter-spacing: .04em; }
  .filtro-org { max-width: 300px; border: 1px solid #D8DEE8; border-radius: 3px;
                padding: .5rem .8rem; font-size: .88rem; font-family: inherit;
                background: white; color: #363F4C; outline: none; font-weight: 600; }
  .filtro-org:focus { border-color: #2ec4a6; }
  .btn-org { border: none; border-radius: 3px; padding: .5rem 1rem; cursor: pointer;
             font-size: .8rem; font-weight: 700; color: #17967c; background: #e2f7f2; }
  .btn-org:hover { background: #d0f0e8; }
  .chip.org { background: #e2f7f2; color: #17967c; }
  .org-item { display: flex; align-items: center; gap: .7rem; padding: .7rem .9rem;
              background: #F5F7FA; border-radius: 3px; margin-bottom: .5rem; }
  .org-item .datos { flex: 1; }
  .org-item .nom { font-weight: 700; font-size: .92rem; }
  .org-item .meta2 { font-size: .78rem; color: #7B8494; }
  .btn-mini { border: none; border-radius: 2px; padding: .3rem .7rem; cursor: pointer;
              font-size: .78rem; font-weight: 700; }
  .btn-mini.rojo { background: #fdeaea; color: #d84343; }
  .aviso-org { grid-column: 1/-1; background: #fffaf0; border: 1px solid #f5e6c8;
               border-radius: 3px; padding: 1rem 1.2rem; font-size: .87rem; color: #8a6d1f; }
  .aviso-org select { max-width: 320px; margin-top: .6rem; }
  .tarea-grupo { grid-column: 1/-1; margin-top: 1.1rem; }
  .tarea-persona { display: flex; align-items: center; gap: .6rem; margin-bottom: .5rem; }
  .tarea-persona .nom { font-size: .95rem; font-weight: 800; cursor: pointer; }
  .tarea-persona .nom:hover { color: #26529E; }
  .tarea-persona .emp { font-size: .78rem; color: #7B8494; }
  .tarea-persona .avatar { width: 30px; height: 30px; font-size: .72rem; margin-bottom: 0; }
  .contador-org { grid-column: 1/-1; display: flex; gap: .8rem; flex-wrap: wrap;
                  margin-bottom: .3rem; }
  .kpi { background: white; border: 1px solid #E3E7EE; border-top: 3px solid #26529E;
         border-radius: 2px; padding: .7rem 1.1rem;
         box-shadow: 0 1px 3px rgba(54,63,76,.10); }
  .kpi .num { font-size: 1.4rem; font-weight: 800; color: #26529E; }
  .kpi .lbl { font-size: .74rem; color: #7B8494; font-weight: 600; text-transform: uppercase; }
  .vacio { color: #A9B9D3; padding: 2.5rem; text-align: center; grid-column: 1/-1; }
  .dia-titulo { grid-column: 1/-1; font-size: .82rem; font-weight: 800; color: #26529E;
                text-transform: uppercase; letter-spacing: .06em; margin-top: .6rem;
                padding: .45rem .75rem; border-radius: 3px; border-left: 4px solid #26529E;
                background: #eef0ff; }
  .dia-titulo.tono-0 { background: #eef0ff; color: #26529E; border-left-color: #26529E; }
  .dia-titulo.tono-1 { background: #f5edff; color: #556D96; border-left-color: #556D96; }
  .dia-titulo.tono-2 { background: #e8f8f3; color: #17866f; border-left-color: #2ec4a6; }
  .dia-titulo.tono-3 { background: #fff0e8; color: #c86235; border-left-color: #ff8a5b; }
  .agenda-toolbar { grid-column: 1/-1; display: flex; justify-content: space-between; align-items: center;
                    gap: .7rem; flex-wrap: wrap; margin-bottom: .2rem; }
  .agenda-vistas { display: flex; gap: .4rem; background: rgba(255,255,255,.75); padding: .25rem;
                   border-radius: 3px; box-shadow: 0 1px 3px rgba(54,63,76,.10); }
  .agenda-vista-btn { border: none; background: transparent; border-radius: 3px; padding: .5rem .8rem;
                      cursor: pointer; font-size: .82rem; font-weight: 700; color: #7c83a8; }
  .agenda-vista-btn.activa { background: white; color: #26529E; box-shadow: 0 1px 2px rgba(54,63,76,.10); }
  .calendario-wrap { grid-column: 1/-1; background: white; border-radius: 18px; padding: 1rem;
                     box-shadow: 0 1px 4px rgba(54,63,76,.10); overflow-x: auto; }
  .calendario-cabecera { display: flex; justify-content: space-between; align-items: center;
                         gap: .7rem; margin-bottom: .9rem; }
  .calendario-cabecera h3 { font-size: 1.05rem; text-transform: capitalize; }
  .cal-nav { border: none; background: #EEEEEE; color: #535b84; border-radius: 3px; width: 34px; height: 34px;
             cursor: pointer; font-size: 1rem; font-weight: 800; }
  .cal-nav:disabled { opacity: .35; cursor: default; }
  .cal-semana, .cal-grid { display: grid; grid-template-columns: repeat(7, minmax(110px, 1fr)); min-width: 770px; }
  .cal-semana div { padding: .5rem; text-align: center; font-size: .72rem; font-weight: 800;
                    color: #7B8494; text-transform: uppercase; }
  .cal-dia { min-height: 112px; border-top: 1px solid #edf0f8; border-right: 1px solid #edf0f8;
             padding: .45rem; background: #fff; }
  .cal-dia:nth-child(7n+1) { border-left: 1px solid #edf0f8; }
  .cal-dia.fuera { background: #fafbfe; color: #bbc0d7; }
  .cal-dia.hoy { background: #f3f5ff; box-shadow: inset 0 0 0 2px #aeb7ff; }
  .cal-num { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
             border-radius: 50%; font-size: .78rem; font-weight: 800; margin-bottom: .3rem; }
  .cal-dia.hoy .cal-num { background: #26529E; color: white; }
  .cal-evento { display: block; width: 100%; border: none; border-left: 3px solid #26529E;
                background: #eef0ff; color: #34419e; border-radius: 6px; padding: .28rem .35rem;
                margin-top: .25rem; text-align: left; font-size: .68rem; line-height: 1.25;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis; cursor: pointer; }
  .cal-evento:nth-of-type(3n+2) { background: #f5edff; color: #713bbd; border-left-color: #556D96; }
  .cal-evento:nth-of-type(3n+3) { background: #e8f8f3; color: #167863; border-left-color: #2ec4a6; }
  .cal-puntos { display: none; gap: 3px; justify-content: center; margin-top: 3px; flex-wrap: wrap; }
  .cal-punto { width: 6px; height: 6px; border-radius: 50%; background: #26529E; }
  .cal-punto:nth-child(3n+2) { background: #556D96; }
  .cal-punto:nth-child(3n+3) { background: #2ec4a6; }
  .dia-detalle { grid-column: 1/-1; background: white; border: 1px solid #E3E7EE;
                 border-top: 3px solid #26529E; border-radius: 3px; padding: 1rem 1.1rem;
                 margin-top: .9rem; }
  .dia-detalle .cabecera-dia { display: flex; justify-content: space-between; align-items: center;
                               gap: .8rem; margin-bottom: .8rem; flex-wrap: wrap; }
  .dia-detalle h4 { font-size: .92rem; color: #26529E; text-transform: capitalize; margin: 0; }
  .btn-agregar-dia { border: none; background: #17967C; color: white; border-radius: 3px;
                     padding: .45rem 1rem; cursor: pointer; font-size: .82rem; font-weight: 700; }
  .btn-agregar-dia:hover { background: #127a65; }
  .busca-contacto { position: relative; }
  .lista-sugerencias { position: absolute; left: 0; right: 0; top: 100%; background: white;
                       border: 1px solid #D8DEE8; border-radius: 3px; max-height: 210px;
                       overflow-y: auto; z-index: 90; display: none;
                       box-shadow: 0 6px 18px rgba(54,63,76,.15); }
  .lista-sugerencias.abierta { display: block; }
  .sug-item { padding: .55rem .8rem; cursor: pointer; font-size: .87rem;
              border-bottom: 1px solid #F0F2F6; }
  .sug-item:last-child { border-bottom: none; }
  .sug-item:hover, .sug-item.marcado { background: #E3EAF5; }
  .sug-item .sug-emp { font-size: .74rem; color: #7B8494; }
  .sug-vacio { padding: .6rem .8rem; font-size: .82rem; color: #A9B9D3; font-style: italic; }
  .elegido { display: inline-flex; align-items: center; gap: .5rem; background: #E3EAF5;
             color: #26529E; border-radius: 3px; padding: .35rem .7rem; font-size: .85rem;
             font-weight: 700; margin-top: .4rem; }
  .elegido button { border: none; background: transparent; color: #26529E; cursor: pointer;
                    font-size: .95rem; line-height: 1; }
  .cal-dia { cursor: pointer; }
  .cal-dia:hover:not(.fuera) { background: #F5F7FA; }
  .dia-detalle .evento { margin-bottom: .6rem; }
  @media (max-width: 620px) {
    .calendario-wrap { overflow-x: visible; }
    .cal-semana, .cal-grid { grid-template-columns: repeat(7, 1fr); min-width: 0; }
    .cal-semana div { font-size: .62rem; padding: .3rem 0; }
    .cal-dia { min-height: 46px; padding: .25rem .1rem; display: flex;
               flex-direction: column; align-items: center; cursor: pointer; }
    .cal-num { width: 24px; height: 24px; font-size: .78rem; margin: 0; }
    .cal-evento { display: none; }
    .cal-puntos { display: flex; }
    .cal-dia.seleccionado { background: #E3EAF5; box-shadow: inset 0 0 0 2px #26529E; }
    .calendario-cabecera h3 { font-size: .95rem; }
  }
  .evento { background: white; border-radius: 4px; padding: 1rem 1.15rem;
            box-shadow: 0 1px 4px rgba(54,63,76,.10); border-left: 5px solid #26529E; }
  .evento .hora { font-size: .78rem; font-weight: 800; color: #26529E; }
  .evento h3 { font-size: 1rem; margin: .2rem 0 .3rem; }
  .nota-evento { font-size: .82rem; color: #4a544e; background: #fffaf0;
                 border: 1px solid #f5e6c8; border-radius: 3px; padding: .5rem .7rem;
                 margin-top: .5rem; line-height: 1.45; white-space: pre-wrap; }
  .asistente { display: block; margin-top: .5rem; padding: .45rem .7rem;
               background: #F5F7FA; border-radius: 3px; }
  .asistente .nom { font-size: .84rem; font-weight: 700; color: #363F4C; cursor: pointer; }
  .asistente .nom:hover { color: #26529E; text-decoration: underline; }
  .asistente .nom.sin-match { color: #7B8494; cursor: default; }
  .asistente .nom.sin-match:hover { color: #7B8494; text-decoration: none; }
  #velo { position: fixed; inset: 0; background: rgba(35,41,70,.5); display: none;
          align-items: flex-start; justify-content: center; padding: 3rem 1rem;
          overflow-y: auto; backdrop-filter: blur(3px); }
  #velo.abierto { display: flex; }
  .ficha { background: white; border-radius: 3px; border-top: 4px solid #26529E; max-width: 680px; width: 100%;
           padding: 1.8rem; box-shadow: 0 1px 20px rgba(54,63,76,.10); }
  .ficha h2 { font-size: 1.25rem; margin-bottom: .15rem; }
  .cerrar { float: right; border: none; background: #EEEEEE; border-radius: 3px;
            padding: .35rem .8rem; cursor: pointer; font-size: .85rem; color: #595959;
            font-weight: 600; }
  .cerrar:hover { opacity: .85; }
  .ventanas { display: flex; gap: .4rem; margin-top: 1.2rem; border-bottom: 2px solid #EEEEEE; }
  .ventana-btn { border: none; background: transparent; padding: .6rem 1rem; cursor: pointer;
                 font-size: .88rem; font-weight: 600; color: #7B8494;
                 border-bottom: 3px solid transparent; margin-bottom: -2px; transition: all .15s; }
  .ventana-btn:hover { color: #363F4C; }
  .ventana-btn.activa.v-info   { color: #26529E; border-bottom-color: #26529E; }
  .ventana-btn.activa.v-notas  { color: #556D96; border-bottom-color: #556D96; }
  .ventana-btn.activa.v-puntos { color: #a37b12; border-bottom-color: #e0a10b; }
  .panel-ventana { display: none; padding-top: 1.1rem; min-height: 220px; }
  .panel-ventana.visible { display: block; }
  .dato { display: flex; justify-content: space-between; font-size: .87rem;
          padding: .45rem 0; border-bottom: 1px dashed #E3E7EE; }
  .dato:last-child { border-bottom: none; }
  .dato .etiqueta { color: #7B8494; }
  .dato .valor { font-weight: 600; text-align: right; max-width: 60%; word-break: break-word; }
  .subtitulo { font-size: .78rem; font-weight: 700; color: #26529E;
               text-transform: uppercase; letter-spacing: .05em; margin: 1.1rem 0 .5rem; }
  .inter { border-left: 4px solid #556D96; padding: .6rem .9rem; margin-bottom: .65rem;
           background: #F5F7FA; border-radius: 0; }
  .inter .fecha { font-size: .72rem; color: #A9B9D3; font-weight: 600; }
  .inter p { font-size: .88rem; margin-top: .25rem; line-height: 1.45; }
  .inter-cabecera { display: flex; justify-content: space-between; align-items: center; gap: .6rem; }
  .inter-acciones { display: flex; gap: .35rem; flex-shrink: 0; }
  .btn-inter { border: none; border-radius: 2px; padding: .28rem .55rem; cursor: pointer;
               font-size: .72rem; font-weight: 700; background: #eceeff; color: #26529E; }
  .btn-inter:hover { opacity: .82; }
  .btn-inter.eliminar { background: #fdeaea; color: #d84343; }
  .editor-nota { margin-top: .55rem; }
  .editor-nota textarea { min-height: 90px; }
  .editor-acciones { display: flex; gap: .45rem; margin-top: .45rem; align-items: center; }
  .editor-acciones select { width: auto; }
  .pendiente { display: flex; gap: .55rem; align-items: baseline; font-size: .88rem;
               margin-bottom: .4rem; padding: .5rem .75rem; border-radius: 3px;
               cursor: pointer; user-select: none; transition: all .15s; }
  .pendiente.abierto { background: #fffaf0; border: 1px solid #f5e6c8; }
  .pendiente.abierto::before { content: "☐"; color: #e0a10b; font-weight: 700; }
  .pendiente.hecho { background: #f4fbf7; border: 1px solid #c4ebd5; color: #595959; }
  .pendiente.hecho::before { content: "✓"; color: #22a35f; font-weight: 800; }
  .pendiente.hecho span { text-decoration: line-through; }
  .pendiente:hover { transform: translateX(2px); }
  .sin-datos { color: #A9B9D3; font-style: italic; font-size: .82rem; padding: 1rem 0; }
  textarea, input[type=text], select { width: 100%; border: 1px solid #D8DEE8; border-radius: 3px;
      padding: .6rem .8rem; font-size: .88rem; font-family: inherit; outline: none;
      background: white; color: #363F4C; }
  textarea:focus, input[type=text]:focus, select:focus { border-color: #26529E; }
  textarea { resize: vertical; min-height: 70px; }
  .campo { margin-bottom: .75rem; }
  .campo label { display: block; font-size: .78rem; font-weight: 700; color: #595959;
                 margin-bottom: .3rem; }
  .dos-cols { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
  .fila-form { display: flex; gap: .5rem; margin-top: .55rem; align-items: center; }
  .fila-form select { width: auto; }
  .btn-guardar { border: none; border-radius: 3px; padding: .55rem 1.2rem; cursor: pointer;
                 font-size: .88rem; font-weight: 700; color: white;
                 background: #26529E; }
  .btn-guardar:disabled { opacity: .5; cursor: wait; }
  .aviso-ia { font-size: .78rem; color: #556D96; margin-top: .45rem; display: none; }
  .historial { margin-top: 1rem; }
  .error-form { color: #d84343; font-size: .8rem; margin-top: .4rem; display: none; }
  .zona-importar { grid-column: 1/-1; background: white; border-radius: 4px;
                   padding: 1.6rem; box-shadow: 0 1px 4px rgba(54,63,76,.10); }
  .zona-importar h3 { font-size: 1.05rem; margin-bottom: .4rem; }
  .zona-importar p { font-size: .85rem; color: #595959; margin-bottom: 1rem; line-height: 1.5; }
  .drop { border: 2px dashed #A9B9D3; border-radius: 3px; padding: 2rem;
          text-align: center; color: #7B8494; font-size: .9rem; cursor: pointer;
          transition: all .15s; }
  .drop:hover, .drop.arrastrando { border-color: #26529E; background: #F5F7FA; color: #26529E; }
  .rev-seccion { grid-column: 1/-1; }
  .rev-titulo { font-size: .82rem; font-weight: 800; color: #26529E;
                text-transform: uppercase; letter-spacing: .06em; margin: 1rem 0 .6rem; }
  .rev-item { background: white; border-radius: 3px; padding: 1rem 1.1rem;
              box-shadow: 0 1px 3px rgba(54,63,76,.10); margin-bottom: .7rem;
              display: flex; gap: .9rem; align-items: flex-start; }
  .rev-item.descartado { opacity: .45; }
  .rev-check { width: 22px; height: 22px; margin-top: .3rem; cursor: pointer; flex-shrink: 0; }
  .rev-campos { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; }
  .rev-campos .full { grid-column: 1/-1; }
  .rev-campos input, .rev-campos select, .rev-campos textarea { padding: .45rem .6rem; font-size: .84rem; }
  .barra-importar { grid-column: 1/-1; display: flex; gap: .7rem; align-items: center;
                    margin-top: 1rem; flex-wrap: wrap; }
  .msj-importar { font-size: .85rem; font-weight: 600; }
  .msj-importar.ok { color: #22a35f; }
  .msj-importar.mal { color: #d84343; }
  .zona-voz { grid-column: 1/-1; background: white; border-radius: 4px; padding: 1.6rem;
              box-shadow: 0 1px 4px rgba(54,63,76,.10); margin-bottom: 1rem;
              display: flex; flex-direction: column; align-items: center; }
  .zona-voz h3 { font-size: 1.05rem; margin-bottom: .4rem; align-self: flex-start; }
  .zona-voz p { font-size: .85rem; color: #595959; margin-bottom: 1.1rem;
                line-height: 1.5; align-self: flex-start; }
  .btn-grabar { width: 128px; height: 128px; border-radius: 50%; border: none; cursor: pointer;
                background: #B03A3A; color: white;
                font-size: .82rem; font-weight: 700; line-height: 1.3; padding: .6rem;
                box-shadow: 0 3px 10px rgba(176,58,58,.28); transition: all .15s; }
  .btn-grabar:hover { transform: scale(1.04); }
  .btn-grabar.grabando { background: linear-gradient(135deg, #d84343, #a32222);
                         animation: latido 1.4s ease-in-out infinite; }
  .btn-grabar.pausado { background: linear-gradient(135deg, #e0a10b, #b8820a); animation: none; }
  .btn-grabar:disabled { opacity: .55; cursor: wait; animation: none; }
  @keyframes latido { 0%,100% { box-shadow: 0 3px 10px rgba(176,58,58,.28); }
                      50% { box-shadow: 0 3px 10px rgba(176,58,58,.28); } }
  .cronometro { font-size: 1.5rem; font-weight: 800; color: #363F4C; margin-top: .8rem;
                font-variant-numeric: tabular-nums; }
  .controles-voz { display: flex; gap: .6rem; margin-top: .9rem; }
  .btn-voz { border: none; border-radius: 3px; padding: .5rem 1.2rem; cursor: pointer;
             font-size: .85rem; font-weight: 700; }
  .btn-voz.pausa { background: #fff5d9; color: #a37b12; }
  .btn-voz.detener { background: #fdeaea; color: #d84343; }
  .btn-voz.cancelar { background: #EEEEEE; color: #595959; }
  .estado-voz { font-size: .85rem; color: #556D96; font-weight: 600; margin-top: .8rem;
                text-align: center; }
  .separador-o { grid-column: 1/-1; text-align: center; color: #A9B9D3; font-size: .8rem;
                 font-weight: 700; margin: .2rem 0 .8rem; }
  .caja-voz-ficha { background: #fdf2f6; border: 1px solid #f6d9e4; border-radius: 3px;
                    padding: .8rem .9rem; margin-bottom: .8rem; text-align: center; }
  .btn-grabar-mini { border: none; border-radius: 3px; padding: .55rem 1.2rem; cursor: pointer;
                     font-size: .85rem; font-weight: 700; color: white;
                     background: #B03A3A; }
  .btn-grabar-mini.grabando { animation: latido 1.4s ease-in-out infinite; }
  .btn-grabar-mini:disabled { opacity: .55; cursor: wait; }
  .transcripcion-caja { grid-column: 1/-1; background: #F5F7FA; border: 1px solid #D8DEE8;
                        border-radius: 3px; padding: 1.1rem; margin-bottom: 1rem; }
  .campo-rev { display: flex; flex-direction: column; gap: .2rem; }
  .campo-rev.full { grid-column: 1/-1; }
  .campo-rev label { font-size: .7rem; font-weight: 700; color: #7B8494;
                     text-transform: uppercase; letter-spacing: .03em; }
  .estado-rev { display: inline-block; font-size: .7rem; font-weight: 700;
                padding: .15rem .55rem; border-radius: 3px; margin-bottom: .35rem; }
  .estado-rev.nuevo { background: #e2f7f2; color: #17967c; }
  .estado-rev.existe { background: #E3EAF5; color: #26529E; }
  .barra-org { grid-column: 1/-1; background: white; border-radius: 3px;
               padding: 1rem 1.2rem; box-shadow: 0 1px 3px rgba(54,63,76,.10);
               margin-bottom: .3rem; }
  .barra-org label { display: block; font-size: .78rem; font-weight: 700;
                     color: #595959; margin-bottom: .35rem; }
  .barra-org select { max-width: 380px; }
  .barra-org .aviso { font-size: .8rem; color: #a37b12; margin-top: .5rem; display: none; }
</style>
</head>
<body>
<div id="velo-menu" onclick="cerrarMenuLateral()"></div>
<nav class="lateral" id="lateral">
  <div class="lateral-cabecera">
    <div class="titulo">Integra Life</div>
    <div class="sub2">tu memoria ejecutiva</div>
  </div>
  <div class="lateral-nav">
    <button class="nav-item activa" data-vista="hoy" onclick="irAVista('hoy')"><span class="ico">◈</span> Hoy</button>
    <button class="nav-item" data-vista="contactos" onclick="irAVista('contactos')"><span class="ico">👤</span> Contactos</button>
    <button class="nav-item" data-vista="empresas" onclick="irAVista('empresas')"><span class="ico">🏢</span> Empresas</button>
    <button class="nav-item" data-vista="agenda" onclick="irAVista('agenda')"><span class="ico">📅</span> Agenda</button>
    <button class="nav-item" data-vista="tareas" onclick="irAVista('tareas')"><span class="ico">☑</span> Tareas</button>
    <button class="nav-item" data-vista="importar" onclick="irAVista('importar')"><span class="ico">🎙</span> Importar audio/archivos</button>
  </div>
  <div class="lateral-pie">Integra Life · v1.0</div>
</nav>

<header>
  <button class="btn-menu" id="btn-menu" onclick="alternarMenuLateral(event)" title="Menú">
    <span></span><span></span><span></span>
  </button>
  <div class="logo">IL</div>
  <div>
    <h1>Integra Life</h1>
    <div class="sub">tu memoria ejecutiva</div>
  </div>
<div class="zona-usuario">
    <div class="menu-usuario">
      <button class="btn-usuario" id="nombre-usuario" onclick="alternarMenuUsuario(event)">Cargando…</button>
      <div class="desplegable" id="menu-usuario">
        <button onclick="abrirConfiguracion(); cerrarMenuUsuario()">⚙ Configuración</button>
        <button class="rojo" onclick="cerrarSesion()">Cerrar sesión</button>
      </div>
    </div>
  </div>
</header>

<div class="barra">
  <div class="titulo-vista" id="titulo-vista">Hoy</div>
  <button class="btn-nuevo" id="btn-nuevo" onclick="abrirFormNuevo()">+ Nuevo contacto</button>
</div>

<div class="barra-busqueda" id="selector-org" style="display:flex;align-items:center;gap:.7rem;flex-wrap:wrap">
  <label class="lbl-filtro">Filtrar por organización</label>
  <select id="filtro-org" class="filtro-org" onchange="cambiarFiltroOrg(this.value)"></select>
</div>

<div class="barra-busqueda" id="barra-busqueda">
  <input type="search" id="buscador" class="buscador" placeholder="Buscar contacto por nombre…" autocomplete="off">
</div>

<div id="contenido" class="grid"></div>

<button class="btn-flotante" id="btn-flotante" title="Grabar nota de voz"
        onclick="grabarRapido()">🎙</button>

<div id="velo"><div class="ficha" id="ficha"></div></div>

<script>
const contenido = document.getElementById("contenido");
const velo = document.getElementById("velo");
const ficha = document.getElementById("ficha");
const btnNuevo = document.getElementById("btn-nuevo");
const barraBusqueda = document.getElementById("barra-busqueda");
const buscador = document.getElementById("buscador");
function localStorage_seguro(clave, valor) {
  try {
    if (valor === undefined) return window.localStorage.getItem(clave);
    window.localStorage.setItem(clave, valor);
  } catch (e) { return null; }
}

let vista = "hoy";
let datosListado = [];
let contactoAbierto = null;
let empresaAbierta = null;
let datosImportados = null;
let filtroOrg = localStorage_seguro("il_filtro_org") || "todas";
let misOrganizaciones = [];

const paletaAvatar = ["#26529E", "#556D96", "#2ec4a6", "#ff8a5b", "#8C3A4E", "#3aa8e0"];
const colorAvatar = n => paletaAvatar[(n || "?").charCodeAt(0) % paletaAvatar.length];
const iniciales = n => (n || "?").split(" ").map(p => p[0]).slice(0, 2).join("").toUpperCase();
const avatarHTML = (d, grande = false) => {
  const clase = "avatar" + (grande ? " avatar-grande" : "");
  if (d.foto_url) {
    return `<img class="${clase}" src="${d.foto_url}" alt="Foto de ${d.nombre || "perfil"}">`;
  }
  return `<div class="${clase}" style="background:${colorAvatar(d.nombre)}">${iniciales(d.nombre)}</div>`;
};

const TITULOS_VISTA = {
  hoy: "Hoy", contactos: "Contactos", empresas: "Empresas",
  agenda: "Agenda", tareas: "Tareas", importar: "Importar audio/archivos",
};

function alternarMenuLateral(ev) {
  if (ev) ev.stopPropagation();
  const abierto = document.getElementById("lateral").classList.toggle("abierto");
  document.getElementById("velo-menu").classList.toggle("abierto", abierto);
  document.getElementById("btn-menu").classList.toggle("abierto", abierto);
}

function cerrarMenuLateral() {
  document.getElementById("lateral").classList.remove("abierto");
  document.getElementById("velo-menu").classList.remove("abierto");
  document.getElementById("btn-menu").classList.remove("abierto");
}

function irAVista(nueva) {
  vista = nueva;
  document.querySelectorAll(".nav-item").forEach(x => {
    x.classList.toggle("activa", x.dataset.vista === nueva);
  });
  const titulo = document.getElementById("titulo-vista");
  if (titulo) titulo.textContent = TITULOS_VISTA[nueva] || "";

  const selOrg = document.getElementById("selector-org");
  if (vista === "hoy") {
    btnNuevo.style.display = "none";
    barraBusqueda.style.display = "none";
    selOrg.style.display = "flex";
  } else if (vista === "importar") {
    btnNuevo.style.display = "none";
    barraBusqueda.style.display = "none";
    selOrg.style.display = "none";
  } else if (vista === "agenda" || vista === "tareas") {
    btnNuevo.style.display = "none";
    barraBusqueda.style.display = "none";
    selOrg.style.display = "flex";
  } else {
    btnNuevo.style.display = "";
    barraBusqueda.style.display = "";
    selOrg.style.display = "flex";
    btnNuevo.textContent = vista === "contactos" ? "+ Nuevo contacto" : "+ Nueva empresa";
    buscador.placeholder = vista === "contactos" ? "Buscar contacto por nombre…" : "Buscar empresa por nombre…";
    buscador.value = "";
  }
  cerrarMenuLateral();
  cargar();
}

velo.onclick = e => { if (e.target === velo) velo.classList.remove("abierto"); };

async function cargar() {
  if (vista === "hoy") { cargarHoy(); return; }
  if (vista === "agenda") { cargarAgenda(); return; }
  if (vista === "importar") { cargarImportar(); return; }
  if (vista === "tareas") { cargarTareas(); return; }
  contenido.innerHTML = "<div class='vacio'>Cargando…</div>";
  const sufijo = "?org=" + filtroOrg;
  const datos = await (await fetch("/" + vista + sufijo)).json();
  datosListado = [...datos].sort((a, b) =>
    (a.nombre || "").localeCompare(b.nombre || "", "es", { sensitivity: "base" })
  );
  mostrarListado();
}

function mostrarListado() {
  const termino = (buscador.value || "").trim().toLocaleLowerCase("es");
  const datos = datosListado.filter(d =>
    (d.nombre || "").toLocaleLowerCase("es").includes(termino)
  );

  if (!datosListado.length) {
    contenido.innerHTML = "<div class='vacio'>Sin registros aún — usa el botón verde para crear el primero</div>";
    return;
  }
  if (!datos.length) {
    contenido.innerHTML = `<div class='vacio'>No se encontraron ${vista === "contactos" ? "contactos" : "empresas"} con ese nombre</div>`;
    return;
  }

  contenido.innerHTML = "";
  datos.forEach(d => {
    const t = document.createElement("div");
    const tipo = (d.relacion_tipo || "otro");
    t.className = "tarjeta " + (vista === "contactos" ? tipo : "empresa");
    if (vista === "contactos") {
      t.innerHTML = `${avatarHTML(d)}
        <h3>${d.nombre}</h3>
        <div class="meta">${d.cargo || "—"} · ${d.empresa || "sin empresa"}</div>
        ${d.relacion_tipo ? `<span class="chip ${tipo}">${d.relacion_tipo}</span>` : ""}
        ${d.relacion_estado ? `<span class="chip estado">${d.relacion_estado}</span>` : ""}
        ${d.organizacion ? `<span class="chip org">${d.organizacion}</span>` : ""}
        <div class="indicadores">
          <span class="badge-pend ${d.pendientes ? "" : "cero"}">${d.pendientes || 0} pendiente${d.pendientes === 1 ? "" : "s"}</span>
          <span>${textoUltimoContacto(d.ultimo_contacto)}</span>
        </div>`;
      t.onclick = () => abrirFicha(d.id);
    } else {
      t.innerHTML = `${avatarHTML(d)}
        <h3>${d.nombre}</h3>
        <div class="meta">${d.nicho || "sin nicho"}</div>
        ${d.descripcion ? `<div class="meta" style="margin-top:.4rem">${d.descripcion}</div>` : ""}
        ${d.organizacion ? `<span class="chip org">${d.organizacion}</span>` : ""}`;
      t.onclick = () => abrirFichaEmpresa(d.id);
    }
    contenido.appendChild(t);
  });
}

buscador.addEventListener("input", mostrarListado);

function fechaBonita(iso) {
  const d = new Date(iso);
  const hoy = new Date(); hoy.setHours(0,0,0,0);
  const fecha = new Date(d); fecha.setHours(0,0,0,0);
  const dif = Math.round((fecha - hoy) / 86400000);
  const dias = ["domingo","lunes","martes","miércoles","jueves","viernes","sábado"];
  const meses = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  let etiqueta = `${dias[d.getDay()]} ${d.getDate()} ${meses[d.getMonth()]}`;
  if (dif === 0) etiqueta = "hoy · " + etiqueta;
  if (dif === 1) etiqueta = "mañana · " + etiqueta;
  return etiqueta;
}

function horaBonita(iso) {
  const d = new Date(iso);
  if (d.getHours() === 0 && d.getMinutes() === 0) return "todo el día";
  return d.toTimeString().slice(0, 5);
}

let eventosAgenda = [];
let vistaAgenda = "calendario";
let diaSeleccionado = null;
let fechaSeleccionada = null;
let mesAgenda = new Date();
mesAgenda.setDate(1);
mesAgenda.setHours(0,0,0,0);

function claveFecha(iso) {
  const d = new Date(iso);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const dia = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${dia}`;
}

function mostrarDetalleEvento(indice) {
  const e = eventosAgenda[indice];
  if (!e) return;
  const asistentes = (e.asistentes || []).map(a => a.nombre || a.email).filter(Boolean);
  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
    <div class="hora" style="font-size:.8rem;font-weight:800;color:#26529E">${fechaBonita(e.inicio)} · ${horaBonita(e.inicio)}</div>
    <h2 style="margin-top:.35rem">${e.titulo}</h2>
    ${e.ubicacion ? `<div class="meta" style="margin-top:.6rem">📍 ${e.ubicacion}</div>` : ""}
    ${e.descripcion ? `<div class="nota-evento">${e.descripcion}</div>` : ""}
    ${asistentes.length ? `<div class="subtitulo">Asistentes</div>${asistentes.map(n => `<div class="dato"><span class="valor" style="max-width:100%;text-align:left">${n}</span></div>`).join("")}` : ""}
    <div style="margin-top:1.4rem;border-top:1px solid #EEEEEE;padding-top:1rem">
      <button class="btn-guardar" style="background:#E3EAF5;color:#26529E" onclick="abrirFormEditarEvento(${indice})">✎ Editar</button>
      <button class="btn-guardar" style="background:#d84343;margin-left:.5rem" onclick="eliminarEvento('${e.id}', ${e.es_google ? "true" : "false"})">🗑 Eliminar</button>
      ${e.es_google ? `<div class="meta" style="margin-top:.6rem">Este evento viene de Google Calendar: los cambios y la eliminación se revierten en la próxima sincronización si no los haces también allá.</div>` : ""}
    </div>
  `;
  velo.classList.add("abierto");
}

function abrirFormEditarEventoDirecto(indice, ev) {
  ev.stopPropagation();
  velo.classList.add("abierto");
  abrirFormEditarEvento(indice);
}

async function eliminarEventoDesdeLista(id, esGoogle, ev) {
  ev.stopPropagation();
  await eliminarEvento(id, esGoogle);
}

function abrirFormEditarEvento(indice) {
  const e = eventosAgenda[indice];
  if (!e) return;
  const d = new Date(e.inicio);
  const fecha = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  const hora = String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
  ficha.innerHTML = `
    <button class="cerrar" onclick="mostrarDetalleEvento(${indice})">← volver</button>
    <h2>Editar evento</h2>
    <div style="margin-top:1.2rem">
      <div class="campo"><label>Título *</label><input type="text" id="ev-titulo" value="${(e.titulo || "").replace(/"/g, "&quot;")}"></div>
      <div class="dos-cols">
        <div class="campo"><label>Fecha (AAAA-MM-DD) *</label><input type="text" id="ev-fecha" value="${fecha}"></div>
        <div class="campo"><label>Hora (HH:MM)</label><input type="text" id="ev-hora" value="${hora}"></div>
      </div>
      <div class="campo"><label>Ubicación</label><input type="text" id="ev-ubicacion" value="${(e.ubicacion || "").replace(/"/g, "&quot;")}"></div>
      <div class="campo"><label>Mi organización (contexto)</label>
        <select id="ev-org">${opcionesOrganizacion(e.organizacion_id)}</select>
      </div>
      <div class="campo"><label>Notas del evento</label><textarea id="ev-desc">${e.descripcion || ""}</textarea></div>
      <button class="btn-guardar" id="btn-ev" onclick="guardarEdicionEvento('${e.id}')">Guardar cambios</button>
      <div class="error-form" id="error-form"></div>
      ${e.es_google ? `<div class="meta" style="margin-top:.7rem">Ojo: al venir de Google Calendar, estos cambios se perderán en la próxima sincronización.</div>` : ""}
    </div>`;
}

async function guardarEdicionEvento(id) {
  const titulo = val("ev-titulo");
  const fecha = val("ev-fecha");
  if (!titulo || !fecha) { mostrarError("El título y la fecha son obligatorios"); return; }
  document.getElementById("btn-ev").disabled = true;
  const r = await fetch("/calendario/evento/" + id, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      titulo: titulo, fecha: fecha, hora: val("ev-hora"),
      ubicacion: val("ev-ubicacion"), descripcion: val("ev-desc"),
      organizacion_id: val("ev-org"),
    }),
  });
  if (r.ok) { velo.classList.remove("abierto"); cargarAgenda(); }
  else { mostrarError("No se pudo guardar"); document.getElementById("btn-ev").disabled = false; }
}

async function eliminarEvento(id, esGoogle) {
  const aviso = esGoogle
    ? "Este evento viene de Google Calendar y reaparecerá en la próxima sincronización. ¿Eliminarlo igual?"
    : "¿Eliminar este evento de la agenda?";
  if (!confirm(aviso)) return;
  await fetch("/calendario/evento/" + id, { method: "DELETE" });
  velo.classList.remove("abierto");
  cargarAgenda();
}

function renderAgenda() {
  contenido.innerHTML = `
    <div class="agenda-toolbar">
      <div class="agenda-vistas">
        <button class="agenda-vista-btn ${vistaAgenda === "calendario" ? "activa" : ""}" onclick="cambiarVistaAgenda('calendario')">▦ Calendario</button>
        <button class="agenda-vista-btn ${vistaAgenda === "lista" ? "activa" : ""}" onclick="cambiarVistaAgenda('lista')">☷ Lista</button>
      </div>
      <div class="meta">${eventosAgenda.length} evento(s) próximos</div>
    </div>`;

  if (vistaAgenda === "calendario") {
    renderCalendarioMensual();
  } else {
    renderAgendaLista();
  }
}

function cambiarVistaAgenda(nueva) {
  vistaAgenda = nueva;
  renderAgenda();
}

function renderAgendaLista() {
  if (!eventosAgenda.length) {
    contenido.insertAdjacentHTML("beforeend", "<div class='vacio'>Sin eventos próximos</div>");
    return;
  }
  let diaActual = "";
  let tono = 0;
  eventosAgenda.forEach((e, indice) => {
    const dia = fechaBonita(e.inicio);
    if (dia !== diaActual) {
      diaActual = dia;
      const h = document.createElement("div");
      h.className = "dia-titulo tono-" + (tono++ % 4);
      h.textContent = "📅 " + dia;
      contenido.appendChild(h);
    }
    const t = document.createElement("div");
    t.className = "evento";
    const asistentesHtml = (e.asistentes || []).map(a => {
      const nombre = a.nombre || a.email;
      if (a.contacto_id) {
        return `<div class="asistente">
          <span class="nom" onclick="abrirFicha('${a.contacto_id}')">${nombre}</span>
        </div>`;
      }
      return `<div class="asistente"><span class="nom sin-match">${nombre}</span></div>`;
    }).join("");
    t.innerHTML = `
      <div class="evento-acciones">
        <button class="btn-ev-accion editar" title="Editar evento"
          onclick="abrirFormEditarEventoDirecto(${indice}, event)">✎</button>
        <button class="btn-ev-accion borrar" title="Eliminar evento"
          onclick="eliminarEventoDesdeLista('${e.id}', ${e.es_google ? "true" : "false"}, event)">🗑</button>
      </div>
      <div class="hora">${horaBonita(e.inicio)}${e.organizacion ? `<span class="chip-google">${e.organizacion}</span>` : ""}</div>
      <h3>${e.titulo}</h3>
      ${e.ubicacion ? `<div class="meta">📍 ${e.ubicacion}</div>` : ""}
      ${e.descripcion ? `<div class="nota-evento">${e.descripcion}</div>` : ""}
      ${asistentesHtml || "<div class='meta' style='margin-top:.4rem'>Sin asistentes registrados</div>"}
    `;
    t.style.cursor = "pointer";
    t.onclick = ev => {
      if (ev.target.closest(".evento-acciones") || ev.target.closest(".asistente")) return;
      mostrarDetalleEvento(indice);
    };
    contenido.appendChild(t);
  });
}

function moverMes(delta) {
  const actual = new Date();
  actual.setDate(1); actual.setHours(0,0,0,0);
  const candidato = new Date(mesAgenda.getFullYear(), mesAgenda.getMonth() + delta, 1);
  if (candidato < actual) return;
  mesAgenda = candidato;
  renderAgenda();
}

function renderCalendarioMensual() {
  const actual = new Date();
  actual.setDate(1); actual.setHours(0,0,0,0);
  const nombreMes = mesAgenda.toLocaleDateString("es-CL", { month: "long", year: "numeric" });
  const wrap = document.createElement("div");
  wrap.className = "calendario-wrap";
  wrap.innerHTML = `
    <div class="calendario-cabecera">
      <button class="cal-nav" onclick="moverMes(-1)" ${mesAgenda <= actual ? "disabled" : ""}>‹</button>
      <h3>${nombreMes}</h3>
      <button class="cal-nav" onclick="moverMes(1)">›</button>
    </div>
    <div class="cal-semana"><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div></div>
    <div class="cal-grid" id="cal-grid"></div>`;
  contenido.appendChild(wrap);

  const grid = wrap.querySelector("#cal-grid");
  const primero = new Date(mesAgenda.getFullYear(), mesAgenda.getMonth(), 1);
  const offset = (primero.getDay() + 6) % 7;
  const inicio = new Date(primero);
  inicio.setDate(primero.getDate() - offset);
  const hoyClave = claveFecha(new Date().toISOString());

  const eventosPorDia = {};
  eventosAgenda.forEach((e, indice) => {
    const k = claveFecha(e.inicio);
    if (!eventosPorDia[k]) eventosPorDia[k] = [];
    eventosPorDia[k].push({ evento: e, indice });
  });

  for (let i = 0; i < 42; i++) {
    const d = new Date(inicio);
    d.setDate(inicio.getDate() + i);
    const k = claveFecha(d.toISOString());
    const celda = document.createElement("div");
    celda.className = "cal-dia";
    if (d.getMonth() !== mesAgenda.getMonth()) celda.classList.add("fuera");
    if (k === hoyClave) celda.classList.add("hoy");
    const delDia = eventosPorDia[k] || [];
    const puntos = delDia.slice(0, 4).map(() => '<span class="cal-punto"></span>').join("");
    celda.innerHTML = `<div class="cal-num">${d.getDate()}</div>
      <div class="cal-puntos">${puntos}</div>`;
    delDia.forEach(item => {
      const b = document.createElement("button");
      b.className = "cal-evento";
      b.title = `${horaBonita(item.evento.inicio)} · ${item.evento.titulo}`;
      b.textContent = `${horaBonita(item.evento.inicio)} · ${item.evento.titulo}`;
      b.onclick = ev => { ev.stopPropagation(); mostrarDetalleEvento(item.indice); };
      celda.appendChild(b);
    });
    celda.dataset.clave = k;
    const iso = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12, 0, 0).toISOString();
    celda.onclick = () => seleccionarDia(k, iso);
    grid.appendChild(celda);
  }

  if (diaSeleccionado) {
    const celdaSel = grid.querySelector(`[data-clave="${diaSeleccionado}"]`);
    if (celdaSel) celdaSel.classList.add("seleccionado");
    pintarDetalleDia(wrap);
  }
}

async function abrirFormEventoNuevo(fecha) {
  const orgInicial = filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : "todas";
  window.contactosEvento = await (await fetch("/contactos?org=" + orgInicial)).json();
  velo.classList.add("abierto");
  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
    <h2>Nuevo evento</h2>
    <div style="margin-top:1.2rem">
      <div class="campo"><label>Título *</label>
        <input type="text" id="nev-titulo" placeholder="Ej: Reunión de coordinación"></div>
      <div class="dos-cols">
        <div class="campo"><label>Fecha (AAAA-MM-DD) *</label>
          <input type="text" id="nev-fecha" value="${fecha}"></div>
        <div class="campo"><label>Hora (HH:MM)</label>
          <input type="text" id="nev-hora" placeholder="09:00"></div>
      </div>
      <div class="campo"><label>Mi organización (contexto)</label>
        <select id="nev-org" onchange="recargarContactosEvento()">${opcionesOrganizacion(filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : null)}</select></div>
      <div class="campo busca-contacto">
        <label>Contacto involucrado</label>
        <input type="text" id="nev-buscar" placeholder="Escribe para buscar entre tus contactos…"
               autocomplete="off" oninput="filtrarSugerencias()" onfocus="filtrarSugerencias()">
        <div class="lista-sugerencias" id="sugerencias"></div>
        <div id="contacto-elegido"></div>
        <input type="hidden" id="nev-contacto" value="">
      </div>
      <div class="campo"><label>Notas del evento</label>
        <textarea id="nev-notas" placeholder="Temas a tratar, objetivo, antecedentes…"></textarea></div>
      <button class="btn-guardar" id="btn-nev" onclick="crearEventoDesdeCalendario()">Crear evento</button>
      <div class="error-form" id="error-form"></div>
    </div>`;
  document.getElementById("nev-titulo").focus();
}

function normalizarBusqueda(t) {
  return (t || "").toString().toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/['\u2018\u2019\u00b4\u0060.]/g, "").trim();
}

async function recargarContactosEvento() {
  const org = document.getElementById("nev-org").value;
  const consulta = org && org !== "externo" ? org : (org === "externo" ? "personal" : "todas");
  window.contactosEvento = await (await fetch("/contactos?org=" + consulta)).json();
  limpiarContactoElegido();
  filtrarSugerencias();
}

function filtrarSugerencias() {
  const campo = document.getElementById("nev-buscar");
  const caja = document.getElementById("sugerencias");
  if (!campo || !caja) return;
  const texto = normalizarBusqueda(campo.value);
  const lista = (window.contactosEvento || []).filter(c => {
    if (!texto) return true;
    return normalizarBusqueda(c.nombre).includes(texto) ||
           normalizarBusqueda(c.empresa).includes(texto) ||
           normalizarBusqueda(c.cargo).includes(texto);
  }).slice(0, 40);

  if (!lista.length) {
    caja.innerHTML = "<div class='sug-vacio'>Sin coincidencias en esta organización</div>";
    caja.classList.add("abierta");
    return;
  }
  caja.innerHTML = lista.map(c => `
    <div class="sug-item" onclick="elegirContactoEvento('${c.id}', '${(c.nombre || "").replace(/'/g, "")}')">
      <div>${c.nombre}</div>
      <div class="sug-emp">${[c.cargo, c.empresa].filter(Boolean).join(" · ") || "sin empresa"}</div>
    </div>`).join("");
  caja.classList.add("abierta");
}

function elegirContactoEvento(id, nombre) {
  document.getElementById("nev-contacto").value = id;
  document.getElementById("nev-buscar").value = "";
  document.getElementById("sugerencias").classList.remove("abierta");
  document.getElementById("contacto-elegido").innerHTML =
    `<span class="elegido">${nombre}<button onclick="limpiarContactoElegido()" title="Quitar">✕</button></span>`;
}

function limpiarContactoElegido() {
  const oculto = document.getElementById("nev-contacto");
  const elegido = document.getElementById("contacto-elegido");
  if (oculto) oculto.value = "";
  if (elegido) elegido.innerHTML = "";
}

document.addEventListener("click", ev => {
  const caja = document.getElementById("sugerencias");
  if (caja && !ev.target.closest(".busca-contacto")) caja.classList.remove("abierta");
});

async function crearEventoDesdeCalendario() {
  const titulo = val("nev-titulo");
  const fecha = val("nev-fecha");
  if (!titulo || !fecha) { mostrarError("El título y la fecha son obligatorios"); return; }
  document.getElementById("btn-nev").disabled = true;
  const org = val("nev-org");
  const r = await fetch("/calendario/evento", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      titulo: titulo,
      fecha: fecha,
      hora: val("nev-hora"),
      contacto_id: document.getElementById("nev-contacto").value || null,
      organizacion_id: org && org !== "externo" ? org : null,
      descripcion: val("nev-notas"),
    }),
  });
  if (r.ok) {
    velo.classList.remove("abierto");
    cargarAgenda();
  } else {
    mostrarError("No se pudo crear el evento");
    document.getElementById("btn-nev").disabled = false;
  }
}

function seleccionarDia(clave, iso) {
  diaSeleccionado = diaSeleccionado === clave ? null : clave;
  fechaSeleccionada = iso;
  renderAgenda();
}

function pintarDetalleDia(wrap) {
  const delDia = eventosAgenda
    .map((e, indice) => ({ evento: e, indice }))
    .filter(x => claveFecha(x.evento.inicio) === diaSeleccionado);

  const caja = document.createElement("div");
  caja.className = "dia-detalle";
  caja.innerHTML = `
    <div class="cabecera-dia">
      <h4>${fechaBonita(fechaSeleccionada)}</h4>
      <button class="btn-agregar-dia" onclick="abrirFormEventoNuevo('${diaSeleccionado}')">+ Agregar evento</button>
    </div>` +
    (delDia.length ? "" : "<div class='hoy-vacio'>Sin eventos este día</div>") +
    delDia.map(x => {
      const e = x.evento;
      const gente = (e.asistentes || []).filter(a => a.nombre || a.email);
      return `<div class="evento" onclick="mostrarDetalleEvento(${x.indice})" style="cursor:pointer">
        <div class="evento-acciones">
          <button class="btn-ev-accion editar" onclick="abrirFormEditarEventoDirecto(${x.indice}, event)">✎</button>
          <button class="btn-ev-accion borrar" onclick="eliminarEventoDesdeLista('${e.id}', ${e.es_google ? "true" : "false"}, event)">🗑</button>
        </div>
        <div class="hora">${horaBonita(e.inicio)}${e.organizacion ? `<span class="chip-google">${e.organizacion}</span>` : ""}</div>
        <h3>${e.titulo}</h3>
        ${e.ubicacion ? `<div class="meta">📍 ${e.ubicacion}</div>` : ""}
        ${gente.length ? `<div class="meta" style="margin-top:.3rem">Con: ${gente.map(a => a.nombre || a.email).join(", ")}</div>` : ""}
      </div>`;
    }).join("");
  wrap.appendChild(caja);
}

async function cargarAgenda() {
  contenido.innerHTML = "<div class='vacio'>Cargando agenda…</div>";
  const r = await fetch("/calendario/agenda?dias=365&org=" + filtroOrg);
  eventosAgenda = await r.json();
  mesAgenda = new Date();
  mesAgenda.setDate(1); mesAgenda.setHours(0,0,0,0);
  renderAgenda();
}

function cargarImportar() {
  datosImportados = null;
  contenido.innerHTML = `
    <div class="zona-voz">
      <h3>Grabar nota de voz</h3>
      <p>Dicta lo que pasó en la reunión. Al detener, Claude analiza el audio y reparte
         la información entre los contactos, empresas y la agenda que correspondan.</p>
      <button class="btn-grabar" id="btn-grabar" onclick="alternarGrabacion()">
        🎙<br>Presione para<br>grabar audio</button>
      <div class="cronometro" id="cronometro" style="display:none">00:00</div>
      <div class="controles-voz" id="controles-voz" style="display:none">
        <button class="btn-voz pausa" id="btn-pausa" onclick="pausarGrabacion()">⏸ Pausar</button>
        <button class="btn-voz detener" onclick="detenerGrabacion()">⏹ Detener y analizar</button>
        <button class="btn-voz cancelar" onclick="cancelarGrabacion()">Cancelar</button>
      </div>
      <div class="estado-voz" id="estado-voz"></div>
    </div>
    <div class="separador-o">— o —</div>
    <div class="zona-importar">
      <h3>Ingresar archivos</h3>
      <p>Sube un archivo de texto (.txt, .csv, .md) con información de contactos o empresas.
         Claude lo analizará y te mostrará lo que encontró para que <strong>revises y confirmes
         antes de crear nada</strong>. Las notas por persona quedan como anotaciones y los
         eventos con fecha se agregan a la Agenda.</p>
      <div class="drop" id="drop" onclick="document.getElementById('archivo-input').click()">
        Haz clic aquí o arrastra un archivo<br>
        <span style="font-size:.78rem">.txt · .csv · .md · .docx · .xlsx · máx 5 MB</span>
      </div>
      <input type="file" id="archivo-input" accept=".txt,.csv,.md,.tsv,.docx,.xlsx,.xlsm" style="display:none"
             onchange="analizarArchivo(this.files[0])">
      <div id="estado-importar" style="margin-top:1rem"></div>
    </div>
    <div id="revision" class="rev-seccion"></div>
  `;
  const drop = document.getElementById("drop");
  drop.ondragover = e => { e.preventDefault(); drop.classList.add("arrastrando"); };
  drop.ondragleave = () => drop.classList.remove("arrastrando");
  drop.ondrop = e => {
    e.preventDefault();
    drop.classList.remove("arrastrando");
    if (e.dataTransfer.files.length) analizarArchivo(e.dataTransfer.files[0]);
  };
}

let grabadora = null;
let trozosAudio = [];
let cronoTimer = null;
let segundosGrabados = 0;
let destinoVoz = null;

function formatoTiempo(s) {
  const m = Math.floor(s / 60), r = s % 60;
  return String(m).padStart(2, "0") + ":" + String(r).padStart(2, "0");
}

function actualizarCrono() {
  segundosGrabados++;
  const el = document.getElementById("cronometro");
  if (el) el.textContent = formatoTiempo(segundosGrabados);
}

async function alternarGrabacion() {
  if (grabadora && grabadora.state !== "inactive") { detenerGrabacion(); return; }
  destinoVoz = null;
  await iniciarGrabacion({
    boton: "btn-grabar", crono: "cronometro",
    controles: "controles-voz", estado: "estado-voz",
  });
}

async function iniciarGrabacion(ids) {
  window.idsVoz = ids;
  const estado = document.getElementById(ids.estado);
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    trozosAudio = [];
    segundosGrabados = 0;
    grabadora = new MediaRecorder(stream);
    grabadora.ondataavailable = e => { if (e.data.size > 0) trozosAudio.push(e.data); };
    grabadora.onstop = () => {
      stream.getTracks().forEach(t => t.stop());
      clearInterval(cronoTimer);
    };
    grabadora.start();
    cronoTimer = setInterval(actualizarCrono, 1000);

    const btn = document.getElementById(ids.boton);
    if (btn) {
      btn.classList.add("grabando");
      btn.innerHTML = ids.boton === "btn-grabar" ? "⏺<br>Grabando…<br>toca para detener" : "⏺ Grabando… (toca para detener)";
    }
    if (ids.crono) { const cr = document.getElementById(ids.crono); if (cr) { cr.style.display = "block"; cr.textContent = "00:00"; } }
    if (ids.controles) { const co = document.getElementById(ids.controles); if (co) co.style.display = "flex"; }
    if (estado) estado.textContent = "Grabando… habla con naturalidad.";
  } catch (e) {
    if (estado) estado.innerHTML = "<span class='msj-importar mal'>No se pudo acceder al micrófono. Revisa los permisos del navegador.</span>";
  }
}

function pausarGrabacion() {
  if (!grabadora) return;
  const ids = window.idsVoz || {};
  const btn = document.getElementById(ids.boton);
  const btnP = document.getElementById("btn-pausa");
  const estado = document.getElementById(ids.estado);
  if (grabadora.state === "recording") {
    grabadora.pause();
    clearInterval(cronoTimer);
    if (btn) { btn.classList.remove("grabando"); btn.classList.add("pausado"); }
    if (btnP) btnP.textContent = "▶ Reanudar";
    if (estado) estado.textContent = "Grabación en pausa.";
  } else if (grabadora.state === "paused") {
    grabadora.resume();
    cronoTimer = setInterval(actualizarCrono, 1000);
    if (btn) { btn.classList.add("grabando"); btn.classList.remove("pausado"); }
    if (btnP) btnP.textContent = "⏸ Pausar";
    if (estado) estado.textContent = "Grabando… habla con naturalidad.";
  }
}

function limpiarUIGrabacion(texto) {
  const ids = window.idsVoz || {};
  clearInterval(cronoTimer);
  const btn = document.getElementById(ids.boton);
  if (btn) {
    btn.classList.remove("grabando", "pausado");
    btn.innerHTML = ids.boton === "btn-grabar"
      ? "🎙<br>Presione para<br>grabar audio"
      : "🎙 Grabar nota de voz";
  }
  const cr = document.getElementById(ids.crono);
  if (cr) cr.style.display = "none";
  const co = document.getElementById(ids.controles);
  if (co) co.style.display = "none";
  const estado = document.getElementById(ids.estado);
  if (estado) estado.textContent = texto || "";
}

function cancelarGrabacion() {
  if (grabadora && grabadora.state !== "inactive") {
    grabadora.onstop = null;
    grabadora.stop();
    if (grabadora.stream) grabadora.stream.getTracks().forEach(t => t.stop());
  }
  grabadora = null;
  trozosAudio = [];
  limpiarUIGrabacion("Grabación cancelada.");
}

function detenerGrabacion() {
  if (!grabadora || grabadora.state === "inactive") return;
  const duracion = segundosGrabados;
  grabadora.onstop = async () => {
    if (grabadora.stream) grabadora.stream.getTracks().forEach(t => t.stop());
    clearInterval(cronoTimer);
    const blob = new Blob(trozosAudio, { type: "audio/webm" });
    grabadora = null;
    await subirNotaVoz(blob, duracion);
  };
  grabadora.stop();
}

function mostrarCargando(texto) {
  velo.classList.add("abierto");
  ficha.innerHTML = `
    <div class="cargando-voz">
      <div class="girador"></div>
      <div class="cargando-texto">${texto}</div>
      <div class="cargando-sub">Esto puede tardar unos segundos</div>
    </div>`;
}

async function subirNotaVoz(blob, duracion) {
  limpiarUIGrabacion("");
  mostrarCargando("Guardando audio y transcribiendo…");

  const form = new FormData();
  form.append("audio", blob, "nota.webm");
  form.append("duracion", duracion);
  form.append("org", filtroOrg);
  let r;
  try {
    r = await fetch("/voz/subir", { method: "POST", body: form });
  } catch (e) {
    ficha.innerHTML = `<button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
      <h2>Error</h2><div class="msj-importar mal" style="display:block;margin-top:1rem">No se pudo enviar el audio.</div>`;
    return;
  }
  if (!r.ok) {
    ficha.innerHTML = `<button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
      <h2>Error</h2><div class="msj-importar mal" style="display:block;margin-top:1rem">No se pudo guardar el audio.</div>`;
    return;
  }
  const nota = await r.json();

  if (!nota.transcripcion) {
    mostrarTranscripcion(nota.id, duracion, nota.transcripcion, nota.aviso);
    return;
  }

  window.notaVozActual = { id: nota.id, duracion: duracion, transcripcion: nota.transcripcion };
  mostrarCargando("Claude está analizando la nota…");
  await analizarNotaVoz(nota.id, true);
}

function mostrarTranscripcion(notaId, duracion, transcripcion, aviso) {
  const destino = destinoVoz;
  const contenedor = destino ? ficha : document.getElementById("revision");
  const texto = transcripcion || "";
  const html = `
    <div class="transcripcion-caja" id="caja-transcripcion">
      <div class="rev-titulo" style="margin-top:0">Nota de voz grabada (${formatoTiempo(duracion)})</div>
      <audio controls src="/voz/${notaId}/audio" style="width:100%;margin-bottom:.8rem"></audio>
      <div class="campo">
        <label>Transcripción ${texto ? "<span style='color:#17967c'>· transcrita automáticamente</span>" : ""}</label>
        <textarea id="txt-transcripcion" style="min-height:110px"
          placeholder="Escribe o pega aquí lo que dijiste en el audio.">${texto}</textarea>
        <div class="meta" style="margin-top:.3rem">Puedes corregir el texto antes de analizarlo.</div>
      </div>
      ${aviso ? `<div class="msj-importar mal" style="display:block;margin-bottom:.6rem">${aviso}</div>` : ""}
      <button class="btn-nuevo" id="btn-analizar-voz" onclick="analizarNotaVoz('${notaId}')">Analizar con Claude</button>
      <button class="btn-voz cancelar" style="margin-left:.5rem" onclick="retranscribir('${notaId}')">↻ Volver a transcribir</button>
      <button class="cerrar" style="float:none;margin-left:.5rem" onclick="${destino ? (destino.tipo === "contacto" ? `abrirFicha('${destino.id}','notas')` : `abrirFichaEmpresa('${destino.id}')`) : "velo.classList.remove('abierto'); cargarImportar()"}">Descartar</button>
      <div class="estado-voz" id="estado-analisis"></div>
    </div>`;
  const volver = destino
    ? (destino.tipo === "contacto" ? `abrirFicha('${destino.id}','notas')` : `abrirFichaEmpresa('${destino.id}')`)
    : "velo.classList.remove('abierto'); cargarImportar()";
  velo.classList.add("abierto");
  ficha.innerHTML = `<button class="cerrar" onclick="${volver}">✕ cerrar</button>
    <h2>Nota de voz</h2>` + html;
  const ta = document.getElementById("txt-transcripcion");
  if (ta && !texto) ta.focus();
}

async function retranscribir(notaId) {
  const estado = document.getElementById("estado-analisis");
  const ta = document.getElementById("txt-transcripcion");
  if (estado) estado.textContent = "✦ Transcribiendo de nuevo…";
  const r = await fetch("/voz/" + notaId + "/retranscribir", { method: "POST" });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    if (estado) estado.innerHTML = `<span class='msj-importar mal'>${err.detail || "No se pudo transcribir"}</span>`;
    return;
  }
  const d = await r.json();
  if (ta) ta.value = d.transcripcion || "";
  if (estado) estado.textContent = "✓ Transcripción actualizada";
}

async function analizarNotaVoz(notaId, automatico) {
  const campo = document.getElementById("txt-transcripcion");
  const estado = document.getElementById("estado-analisis");
  const btn = document.getElementById("btn-analizar-voz");

  let texto = "";
  if (campo) {
    texto = campo.value.trim();
    if (!texto) {
      if (estado) estado.innerHTML = "<span class='msj-importar mal'>Escribe la transcripción para poder analizarla</span>";
      return;
    }
    if (btn) btn.disabled = true;
    if (estado) estado.textContent = "✦ Claude está analizando la nota…";
    await fetch("/voz/" + notaId + "/transcripcion", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcripcion: texto }),
    });
  }

  const r = await fetch("/voz/" + notaId + "/analizar", { method: "POST" });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    const msg = err.detail || "Error al analizar";
    if (automatico) {
      const n = window.notaVozActual || {};
      mostrarTranscripcion(notaId, n.duracion || 0, n.transcripcion || "", msg);
    } else if (estado) {
      estado.innerHTML = `<span class='msj-importar mal'>${msg}</span>`;
      if (btn) btn.disabled = false;
    }
    return;
  }
  const analisis = await r.json();

  datosImportados = {
    organizacion_id: filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : null,
    organizacion_nombre: null,
    empresas: (analisis.empresas || []).map(e => ({
      nombre: e.nombre, nicho: e.nicho, descripcion: e.resumen,
      id_existente: e.id_existente, nombre_existente: e.nombre_existente,
      accion: e.id_existente ? "reutilizar" : "crear",
      notas_empresa: [e.resumen, ...(e.datos_clave || [])].filter(Boolean).join(". "),
    })),
    contactos: (analisis.contactos || []).map(c => ({
      nombre: c.nombre, cargo: c.cargo, email: null, telefono: null,
      empresa_nombre: c.empresa_nombre, relacion_tipo: null,
      notas: [c.resumen, ...(c.temas_pendientes || [])].filter(Boolean).join(". "),
      id_existente: c.id_existente, nombre_existente: c.nombre_existente,
      accion: c.id_existente ? "actualizar" : "crear",
    })),
    eventos: analisis.eventos || [],
  };

  if (destinoVoz) {
    await aplicarNotaEnFicha(analisis);
    return;
  }
  mostrarRevisionEnModal(analisis);
}

function mostrarRevisionEnModal(analisis) {
  const n = window.notaVozActual || {};
  velo.classList.add("abierto");
  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto'); cargarImportar()">✕ cerrar</button>
    <h2>Revisa lo que encontró Claude</h2>
    ${n.id ? `<audio controls src="/voz/${n.id}/audio" style="width:100%;margin-top:.9rem"></audio>` : ""}
    <div class="inter" style="margin-top:.9rem">
      <div class="fecha">Resumen de la nota</div>
      <p>${(analisis.resumen_general || "(sin resumen)").replace(/`/g, "")}</p>
    </div>
    ${n.transcripcion ? `<details style="margin-top:.6rem">
      <summary style="cursor:pointer;font-size:.82rem;color:#26529E;font-weight:700">Ver transcripción</summary>
      <div class="meta" style="margin-top:.5rem;line-height:1.5">${n.transcripcion.replace(/</g, "&lt;")}</div>
      <button class="btn-voz cancelar" style="margin-top:.5rem"
        onclick="mostrarTranscripcion('${n.id}', ${n.duracion || 0}, ${JSON.stringify(n.transcripcion || "")}, null)">✎ Corregir y volver a analizar</button>
    </details>` : ""}
    <div id="revision"></div>`;
  mostrarRevision();
  ficha.scrollTop = 0;
}

async function aplicarNotaEnFicha(analisis) {
  const d = destinoVoz;
  const texto = [analisis.resumen_general,
    ...(analisis.contactos || []).map(c => c.resumen),
    ...(analisis.contactos || []).flatMap(c => c.temas_pendientes || []),
    ...(analisis.empresas || []).map(e => e.resumen),
    ...(analisis.empresas || []).flatMap(e => e.datos_clave || []),
  ].filter(Boolean).join(". ");

  const cuerpo = d.tipo === "contacto"
    ? { contacto_id: d.id, tipo: "nota", contenido_raw: "Nota de voz: " + texto }
    : { empresa_id: d.id, tipo: "nota", contenido_raw: "Nota de voz: " + texto };
  await fetch("/interacciones", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cuerpo),
  });

  const eventos = (analisis.eventos || []).filter(ev => ev.fecha);
  const id = d.id, tipo = d.tipo;
  const estado = document.getElementById("estado-analisis");

  if (!eventos.length) {
    destinoVoz = null;
    if (estado) estado.textContent = "✓ Nota guardada. Claude está procesando el resumen…";
    setTimeout(() => {
      if (tipo === "contacto") abrirFicha(id, "notas");
      else abrirFichaEmpresa(id);
    }, 6000);
    return;
  }

  window.eventosPropuestos = eventos;
  window.destinoEventos = { id: id, tipo: tipo };
  destinoVoz = null;
  if (estado) estado.textContent = "✓ Nota guardada. Revisa los eventos detectados:";

  const filas = eventos.map((ev, i) => `
    <div class="rev-item" id="ev-prop-${i}">
      <input type="checkbox" class="rev-check" id="cev-${i}" checked
        onchange="alternarItem('ev-prop-${i}', this.checked)">
      <div style="flex:1">
        <span class="estado-rev nuevo">+ Nuevo evento</span>
        <div class="rev-campos">
          <div class="campo-rev full"><label>Título *</label>
            <input type="text" id="pev-titulo-${i}" value="${(ev.titulo || "").replace(/"/g, "&quot;")}"></div>
          <div class="campo-rev"><label>Fecha (AAAA-MM-DD) *</label>
            <input type="text" id="pev-fecha-${i}" value="${ev.fecha || ""}"></div>
          <div class="campo-rev"><label>Hora (HH:MM)</label>
            <input type="text" id="pev-hora-${i}" value="${ev.hora || ""}"></div>
          <div class="campo-rev full"><label>Notas</label>
            <input type="text" id="pev-notas-${i}" value="${(ev.notas || "").replace(/"/g, "&quot;")}"></div>
        </div>
      </div>
    </div>`).join("");

  document.getElementById("caja-transcripcion").insertAdjacentHTML("afterend", `
    <div id="eventos-propuestos">
      <div class="rev-titulo">Eventos detectados en la nota — confirma cuáles agendar</div>
      ${filas}
      <div class="barra-importar">
        <button class="btn-nuevo" id="btn-crear-eventos" onclick="crearEventosPropuestos()">Agregar a la agenda</button>
        <button class="cerrar" style="float:none" onclick="volverDeEventos()">Omitir</button>
        <span class="msj-importar" id="msj-eventos"></span>
      </div>
    </div>`);
}

function volverDeEventos() {
  const d = window.destinoEventos || {};
  if (d.tipo === "contacto") abrirFicha(d.id, "notas");
  else if (d.tipo === "empresa") abrirFichaEmpresa(d.id);
  else cargarImportar();
}

async function crearEventosPropuestos() {
  const btn = document.getElementById("btn-crear-eventos");
  const msj = document.getElementById("msj-eventos");
  btn.disabled = true;
  msj.textContent = "Creando…";
  msj.className = "msj-importar";

  const d = window.destinoEventos || {};
  const org = filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : null;
  let creados = 0, errores = 0;

  for (let i = 0; i < (window.eventosPropuestos || []).length; i++) {
    const chk = document.getElementById("cev-" + i);
    if (!chk || !chk.checked) continue;
    const titulo = document.getElementById("pev-titulo-" + i).value.trim();
    const fecha = document.getElementById("pev-fecha-" + i).value.trim();
    if (!titulo || !fecha) continue;
    const r = await fetch("/calendario/evento", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: titulo,
        fecha: fecha,
        hora: document.getElementById("pev-hora-" + i).value.trim() || null,
        contacto_id: d.tipo === "contacto" ? d.id : null,
        organizacion_id: org,
        descripcion: document.getElementById("pev-notas-" + i).value.trim() || "Desde nota de voz",
      }),
    });
    if (r.ok) creados++; else errores++;
  }

  msj.className = "msj-importar " + (errores ? "mal" : "ok");
  msj.textContent = `${creados} evento(s) agregado(s) a la agenda` +
    (errores ? ` · ${errores} con error` : "");
  setTimeout(volverDeEventos, 2500);
}

async function grabarParaContacto(id) {
  destinoVoz = { tipo: "contacto", id: id };
  const btn = document.getElementById("btn-voz-ficha");
  if (grabadora && grabadora.state !== "inactive") { detenerGrabacion(); return; }
  await iniciarGrabacion({ boton: "btn-voz-ficha", crono: "crono-ficha",
                           controles: "controles-ficha", estado: "estado-voz-ficha" });
}

async function grabarParaEmpresa(id) {
  destinoVoz = { tipo: "empresa", id: id };
  if (grabadora && grabadora.state !== "inactive") { detenerGrabacion(); return; }
  await iniciarGrabacion({ boton: "btn-voz-ficha", crono: "crono-ficha",
                           controles: "controles-ficha", estado: "estado-voz-ficha" });
}

function cajaVozFicha(accion) {
  return `
    <div class="caja-voz-ficha">
      <button class="btn-grabar-mini" id="btn-voz-ficha" onclick="${accion}">🎙 Grabar nota de voz</button>
      <div class="cronometro" id="crono-ficha" style="display:none;font-size:1.1rem">00:00</div>
      <div class="controles-voz" id="controles-ficha" style="display:none;justify-content:center">
        <button class="btn-voz pausa" id="btn-pausa" onclick="pausarGrabacion()">⏸ Pausar</button>
        <button class="btn-voz detener" onclick="detenerGrabacion()">⏹ Detener</button>
        <button class="btn-voz cancelar" onclick="cancelarGrabacion()">Cancelar</button>
      </div>
      <div class="estado-voz" id="estado-voz-ficha"></div>
    </div>`;
}

async function analizarArchivo(archivo) {
  if (!archivo) return;
  const estado = document.getElementById("estado-importar");
  estado.innerHTML = "<span class='msj-importar' style='color:#556D96'>✦ Claude está analizando el archivo…</span>";
  document.getElementById("revision").innerHTML = "";

  const form = new FormData();
  form.append("archivo", archivo);
  form.append("org", filtroOrg);
  const r = await fetch("/importar/analizar", { method: "POST", body: form });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    estado.innerHTML = `<span class='msj-importar mal'>${err.detail || "Error al analizar el archivo"}</span>`;
    return;
  }
  datosImportados = await r.json();
  const nE = datosImportados.empresas.length,
        nC = datosImportados.contactos.length,
        nV = (datosImportados.eventos || []).length;
  if (!nE && !nC && !nV) {
    estado.innerHTML = "<span class='msj-importar mal'>No se encontraron contactos, empresas ni eventos en el archivo</span>";
    return;
  }
  estado.innerHTML = `<span class='msj-importar ok'>Se encontraron ${nE} empresa(s), ${nC} contacto(s) y ${nV} evento(s). Revisa, corrige y confirma:</span>`;
  mostrarRevision();
}

function opcionesOrgImport(seleccionada, idSelect) {
  const opts = misOrganizaciones.map(o =>
    `<option value="${o.id}" ${seleccionada === o.id ? "selected" : ""}>${o.nombre}</option>`
  ).join("");
  return `<option value="">— elegir —</option>${opts}` +
    `<option value="externo" ${seleccionada === "externo" ? "selected" : ""}>Externo / Personal</option>`;
}

function orgGlobal() {
  const s = document.getElementById("org-global");
  return s ? s.value : "";
}

function cambiarOrgGlobal() {
  const valor = orgGlobal();
  document.querySelectorAll(".org-fila").forEach(s => { s.value = valor; });
  validarOrg();
}

function validarOrg() {
  const btn = document.getElementById("btn-confirmar");
  const aviso = document.getElementById("aviso-org-import");
  const falta = !orgGlobal();
  if (btn) btn.disabled = falta;
  if (aviso) aviso.style.display = falta ? "block" : "none";
}

function mostrarRevision() {
  const rev = document.getElementById("revision");
  const orgDetectada = datosImportados.organizacion_id ||
    (filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : "");
  let html = "";

  html += `
    <div class="barra-org">
      <label>¿A qué organización pertenece todo lo de este archivo? *</label>
      <select id="org-global" onchange="cambiarOrgGlobal()">${opcionesOrgImport(orgDetectada)}</select>
      ${datosImportados.organizacion_nombre
        ? `<div class="meta" style="margin-top:.4rem">Detectada automáticamente en el archivo: <strong>${datosImportados.organizacion_nombre}</strong></div>`
        : ""}
      <div class="aviso" id="aviso-org-import">Elige una organización (o "Externo / Personal") para poder crear los registros.</div>
    </div>`;

  if (datosImportados.empresas.length) {
    html += "<div class='rev-titulo'>Empresas detectadas</div>";
    datosImportados.empresas.forEach((e, i) => {
      const existe = e.accion === "reutilizar";
      html += `
      <div class="rev-item" id="re-${i}">
        <input type="checkbox" class="rev-check" id="ce-${i}" checked onchange="alternarItem('re-${i}', this.checked)">
        <div style="flex:1">
          <span class="estado-rev ${existe ? "existe" : "nuevo"}">${existe ? "↻ Ya existe: " + e.nombre_existente : "+ Nueva empresa"}</span>
          <div class="rev-campos">
            <div class="campo-rev"><label>Nombre *</label>
              <input type="text" id="e-nombre-${i}" value="${e.nombre || ""}"></div>
            <div class="campo-rev"><label>Nicho</label>
              <input type="text" id="e-nicho-${i}" value="${e.nicho || ""}"></div>
            <div class="campo-rev full"><label>Descripción</label>
              <input type="text" id="e-desc-${i}" value="${e.descripcion || ""}"></div>
            <div class="campo-rev full"><label>Organización</label>
              <select class="org-fila" id="e-org-${i}">${opcionesOrgImport(orgDetectada)}</select></div>
          </div>
        </div>
      </div>`;
    });
  }

  if (datosImportados.contactos.length) {
    html += "<div class='rev-titulo'>Contactos detectados</div>";
    datosImportados.contactos.forEach((c, i) => {
      const tipos = ["", "cliente", "proveedor", "socio", "empresario", "otro"];
      const opts = tipos.map(t =>
        `<option value="${t}" ${c.relacion_tipo === t ? "selected" : ""}>${t || "— elegir —"}</option>`
      ).join("");
      const existe = c.accion === "actualizar";
      html += `
      <div class="rev-item" id="rc-${i}">
        <input type="checkbox" class="rev-check" id="cc-${i}" checked onchange="alternarItem('rc-${i}', this.checked)">
        <div style="flex:1">
          <span class="estado-rev ${existe ? "existe" : "nuevo"}">${existe ? "↻ Ya existe: se agregará a " + c.nombre_existente : "+ Nuevo contacto"}</span>
          <div class="rev-campos">
            <div class="campo-rev"><label>Nombre *</label>
              <input type="text" id="c-nombre-${i}" value="${c.nombre || ""}"></div>
            <div class="campo-rev"><label>Cargo</label>
              <input type="text" id="c-cargo-${i}" value="${c.cargo || ""}"></div>
            <div class="campo-rev"><label>Email</label>
              <input type="text" id="c-email-${i}" value="${c.email || ""}"></div>
            <div class="campo-rev"><label>Teléfono</label>
              <input type="text" id="c-telefono-${i}" value="${c.telefono || ""}"></div>
            <div class="campo-rev"><label>Empresa donde trabaja</label>
              <input type="text" id="c-empresa-${i}" value="${c.empresa_nombre || ""}"></div>
            <div class="campo-rev"><label>Tipo de relación</label>
              <select id="c-tipo-${i}">${opts}</select></div>
            <div class="campo-rev full"><label>Organización</label>
              <select class="org-fila" id="c-org-${i}">${opcionesOrgImport(orgDetectada)}</select></div>
            <div class="campo-rev full"><label>Notas y tareas de esta persona</label>
              <textarea id="c-notas-${i}" style="min-height:56px">${c.notas || ""}</textarea></div>
          </div>
        </div>
      </div>`;
    });
  }

  if (datosImportados.eventos && datosImportados.eventos.length) {
    html += "<div class='rev-titulo'>Eventos detectados (se agregan a la Agenda)</div>";
    datosImportados.eventos.forEach((ev, i) => {
      html += `
      <div class="rev-item" id="rv-${i}">
        <input type="checkbox" class="rev-check" id="cv-${i}" checked onchange="alternarItem('rv-${i}', this.checked)">
        <div style="flex:1">
          <span class="estado-rev nuevo">+ Nuevo evento</span>
          <div class="rev-campos">
            <div class="campo-rev full"><label>Título *</label>
              <input type="text" id="v-titulo-${i}" value="${ev.titulo || ""}"></div>
            <div class="campo-rev"><label>Fecha (AAAA-MM-DD) *</label>
              <input type="text" id="v-fecha-${i}" value="${ev.fecha || ""}"></div>
            <div class="campo-rev"><label>Hora (HH:MM)</label>
              <input type="text" id="v-hora-${i}" value="${ev.hora || ""}"></div>
            <div class="campo-rev"><label>Contacto involucrado</label>
              <input type="text" id="v-contacto-${i}" value="${ev.contacto_nombre || ""}"></div>
            <div class="campo-rev"><label>Organización</label>
              <select class="org-fila" id="v-org-${i}">${opcionesOrgImport(orgDetectada)}</select></div>
            <div class="campo-rev full"><label>Notas del evento</label>
              <input type="text" id="v-notas-${i}" value="${ev.notas || ""}"></div>
          </div>
        </div>
      </div>`;
    });
  }

  html += `
    <div class="barra-importar">
      <button class="btn-nuevo" id="btn-confirmar" onclick="confirmarImportacion()">Crear seleccionados</button>
      <span class="msj-importar" id="msj-final"></span>
    </div>`;
  rev.innerHTML = html;
  validarOrg();
}

function alternarItem(id, activo) {
  document.getElementById(id).classList.toggle("descartado", !activo);
}

async function confirmarImportacion() {
  if (!orgGlobal()) { validarOrg(); return; }
  const btn = document.getElementById("btn-confirmar");
  const msj = document.getElementById("msj-final");
  btn.disabled = true;
  msj.textContent = "Creando…";
  msj.className = "msj-importar";

  const orgReal = v => (v && v !== "externo") ? v : null;
  let creadasE = 0, reusadasE = 0, creadosC = 0, actualizadosC = 0;
  let notas = 0, eventos = 0, errores = 0;
  const mapaEmpresas = {};
  const mapaContactos = {};

  // Empresas
  for (let i = 0; i < datosImportados.empresas.length; i++) {
    if (!document.getElementById("ce-" + i).checked) continue;
    const e = datosImportados.empresas[i];
    const nombre = document.getElementById("e-nombre-" + i).value.trim();
    if (!nombre) continue;
    const org = orgReal(document.getElementById("e-org-" + i).value);

    if (e.id_existente) {
      mapaEmpresas[nombre.toLowerCase()] = e.id_existente;
      reusadasE++;
      continue;
    }
    const r = await fetch("/empresas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre: nombre,
        nicho: document.getElementById("e-nicho-" + i).value.trim() || null,
        descripcion: document.getElementById("e-desc-" + i).value.trim() || null,
        organizacion_id: org,
      }),
    });
    if (r.ok) {
      const creada = await r.json();
      mapaEmpresas[nombre.toLowerCase()] = creada.id;
      creadasE++;
    } else errores++;
  }

  // Contactos
  for (let i = 0; i < datosImportados.contactos.length; i++) {
    if (!document.getElementById("cc-" + i).checked) continue;
    const c = datosImportados.contactos[i];
    const nombre = document.getElementById("c-nombre-" + i).value.trim();
    if (!nombre) continue;
    const org = orgReal(document.getElementById("c-org-" + i).value);
    const empresaNombre = document.getElementById("c-empresa-" + i).value.trim().toLowerCase();
    const email = document.getElementById("c-email-" + i).value.trim();
    const notaTexto = document.getElementById("c-notas-" + i).value.trim();

    let contactoId = c.id_existente || null;
    const empresaId = mapaEmpresas[empresaNombre] || c.empresa_id_existente || null;

    if (contactoId) {
      actualizadosC++;
    } else {
      const r = await fetch("/contactos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nombre: nombre,
          cargo: document.getElementById("c-cargo-" + i).value.trim() || null,
          telefono: document.getElementById("c-telefono-" + i).value.trim() || null,
          relacion_tipo: document.getElementById("c-tipo-" + i).value || null,
          empresa_id: empresaId,
          organizacion_id: org,
          emails: email ? [email] : [],
        }),
      });
      if (r.ok) {
        const creado = await r.json();
        contactoId = creado.id;
        creadosC++;
      } else { errores++; continue; }
    }
    mapaContactos[nombre.toLowerCase()] = contactoId;

    if (notaTexto && contactoId) {
      const rn = await fetch("/interacciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contacto_id: contactoId,
          tipo: "nota",
          contenido_raw: "Importado desde archivo: " + notaTexto,
        }),
      });
      if (rn.ok) notas++; else errores++;
    }
  }

  // Eventos
  if (datosImportados.eventos) {
    for (let i = 0; i < datosImportados.eventos.length; i++) {
      if (!document.getElementById("cv-" + i).checked) continue;
      const ev = datosImportados.eventos[i];
      const titulo = document.getElementById("v-titulo-" + i).value.trim();
      const fecha = document.getElementById("v-fecha-" + i).value.trim();
      if (!titulo || !fecha) continue;
      const org = orgReal(document.getElementById("v-org-" + i).value);
      const contactoNombre = document.getElementById("v-contacto-" + i).value.trim().toLowerCase();
      const rv = await fetch("/calendario/evento", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          titulo: titulo,
          fecha: fecha,
          hora: document.getElementById("v-hora-" + i).value.trim() || null,
          contacto_id: mapaContactos[contactoNombre] || ev.contacto_id_existente || null,
          organizacion_id: org,
          descripcion: document.getElementById("v-notas-" + i).value.trim() || "Importado desde archivo",
        }),
      });
      if (rv.ok) eventos++; else errores++;
    }
  }

  msj.className = "msj-importar " + (errores ? "mal" : "ok");
  const partes = [];
  if (creadasE) partes.push(creadasE + " empresa(s) nueva(s)");
  if (reusadasE) partes.push(reusadasE + " empresa(s) reutilizada(s)");
  if (creadosC) partes.push(creadosC + " contacto(s) nuevo(s)");
  if (actualizadosC) partes.push(actualizadosC + " contacto(s) existente(s) actualizado(s)");
  if (notas) partes.push(notas + " nota(s)");
  if (eventos) partes.push(eventos + " evento(s)");
  msj.textContent = "Listo: " + (partes.join(", ") || "sin cambios") +
    (errores ? " · " + errores + " con error" : "");

  cargarOrganizaciones();
  setTimeout(() => {
    velo.classList.remove("abierto");
    cargarImportar();
  }, 3000);
}

async function abrirFormNuevo() {
  velo.classList.add("abierto");
  if (vista === "contactos") {
    const empresas = await (await fetch("/empresas")).json();
    const opciones = empresas.map(e => `<option value="${e.id}">${e.nombre}</option>`).join("");
    ficha.innerHTML = `
      <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
      <h2>Nuevo contacto</h2>
      <div style="margin-top:1.2rem">
        <div class="campo"><label>Nombre *</label><input type="text" id="f-nombre" placeholder="Ej: María González"></div>
        <div class="dos-cols">
          <div class="campo"><label>Cargo</label><input type="text" id="f-cargo" placeholder="Ej: Gerente Comercial"></div>
          <div class="campo"><label>Tipo de relación</label>
            <select id="f-tipo">
              <option value="">— elegir —</option>
              <option value="cliente">Cliente</option>
              <option value="proveedor">Proveedor</option>
              <option value="socio">Socio</option>
              <option value="empresario">Empresario</option>
              <option value="otro">Otro</option>
            </select>
          </div>
        </div>
        <div class="dos-cols">
          <div class="campo"><label>Empresa donde trabaja</label>
            <select id="f-empresa"><option value="">— sin empresa —</option>${opciones}</select>
          </div>
          <div class="campo"><label>Mi organización (contexto)</label>
            <select id="f-org">${opcionesOrganizacion(filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : null)}</select>
          </div>
        </div>
        <div class="campo"><label>Nicho</label><input type="text" id="f-nicho" placeholder="Ej: construcción"></div>
        <div class="dos-cols">
          <div class="campo"><label>Email</label><input type="text" id="f-email" placeholder="nombre@empresa.cl"></div>
          <div class="campo"><label>Teléfono</label><input type="text" id="f-telefono" placeholder="+56 9 ..."></div>
        </div>
        <div class="campo"><label>LinkedIn</label><input type="text" id="f-linkedin" placeholder="https://linkedin.com/in/..."></div>
        <div class="campo"><label>Notas generales</label><textarea id="f-notas" placeholder="Cómo se conocieron, contexto, estilo de la persona…"></textarea></div>
        <button class="btn-guardar" id="btn-crear" onclick="crearContacto()">Crear contacto</button>
        <div class="error-form" id="error-form"></div>
      </div>`;
  } else {
    ficha.innerHTML = `
      <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
      <h2>Nueva empresa</h2>
      <div style="margin-top:1.2rem">
        <div class="campo"><label>Nombre *</label><input type="text" id="f-nombre" placeholder="Ej: Constructora Andes"></div>
        <div class="dos-cols">
          <div class="campo"><label>Nicho</label><input type="text" id="f-nicho" placeholder="Ej: minería"></div>
          <div class="campo"><label>Sitio web</label><input type="text" id="f-web" placeholder="https://…"></div>
        </div>
        <div class="campo"><label>Mi organización (contexto)</label>
          <select id="f-org-emp">${opcionesOrganizacion(filtroOrg !== "todas" && filtroOrg !== "personal" ? filtroOrg : null)}</select>
        </div>
        <div class="campo"><label>Descripción</label><textarea id="f-desc" placeholder="A qué se dedica, tamaño, relación con ustedes…"></textarea></div>
        <button class="btn-guardar" id="btn-crear" onclick="crearEmpresa()">Crear empresa</button>
        <div class="error-form" id="error-form"></div>
      </div>`;
  }
}

const val = id => document.getElementById(id).value.trim() || null;

async function crearContacto() {
  const nombre = val("f-nombre");
  if (!nombre) { mostrarError("El nombre es obligatorio"); return; }
  document.getElementById("btn-crear").disabled = true;
  const email = val("f-email");
  const r = await fetch("/contactos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: nombre, cargo: val("f-cargo"), relacion_tipo: val("f-tipo"),
      empresa_id: val("f-empresa"), nicho: val("f-nicho"),
      organizacion_id: val("f-org"),
      telefono: val("f-telefono"), linkedin_url: val("f-linkedin"),
      notas_generales: val("f-notas"),
      emails: email ? [email] : [],
    }),
  });
  if (r.ok) { velo.classList.remove("abierto"); cargarOrganizaciones(); cargar(); }
  else { mostrarError("No se pudo crear — revisa los datos"); document.getElementById("btn-crear").disabled = false; }
}

async function crearEmpresa() {
  const nombre = val("f-nombre");
  if (!nombre) { mostrarError("El nombre es obligatorio"); return; }
  document.getElementById("btn-crear").disabled = true;
  const r = await fetch("/empresas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: nombre, nicho: val("f-nicho"),
      sitio_web: val("f-web"), descripcion: val("f-desc"),
      organizacion_id: val("f-org-emp"),
    }),
  });
  if (r.ok) { velo.classList.remove("abierto"); cargarOrganizaciones(); cargar(); }
  else { mostrarError("No se pudo crear — revisa los datos"); document.getElementById("btn-crear").disabled = false; }
}

function mostrarError(msg) {
  const e = document.getElementById("error-form");
  e.textContent = msg;
  e.style.display = "block";
}

function cambiarVentana(nombre) {
  document.querySelectorAll(".ventana-btn").forEach(b => b.classList.remove("activa"));
  document.querySelector(".ventana-btn.v-" + nombre).classList.add("activa");
  document.querySelectorAll(".panel-ventana").forEach(p => p.classList.remove("visible"));
  document.getElementById("pv-" + nombre).classList.add("visible");
}

async function abrirFicha(id, ventanaInicial) {
  contactoAbierto = id;
  ficha.innerHTML = "Cargando…";
  velo.classList.add("abierto");
  const c = await (await fetch("/contactos/" + id)).json();
  window.contactoActual = c;
  const inter = await (await fetch("/interacciones/contacto/" + id)).json();
  window.interaccionesActuales = inter;
  const reuniones = await (await fetch("/calendario/contacto/" + id)).json();

  let pendientesHtml = "";
  let totalPend = 0, totalHechos = 0;
  inter.forEach(i => {
    (i.temas_pendientes || []).forEach((t, idx) => {
      totalPend++;
      if (t.hecho) totalHechos++;
      pendientesHtml += `<div class="pendiente ${t.hecho ? "hecho" : "abierto"}"
        onclick="alternarTema('${i.id}', ${idx}, event)"><span>${t.texto}</span></div>`;
    });
  });

  const datosInfo = [
    ["Cargo", c.cargo], ["Empresa", c.empresa], ["Mi organizacion", c.organizacion],
    ["Nicho", c.nicho],
    ["Teléfono", c.telefono], ["LinkedIn", c.linkedin_url],
    ["Emails", (c.emails || []).join(" · ")], ["Notas", c.notas_generales],
  ].filter(d => d[1]);

  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
    <button class="cerrar" style="margin-right:.4rem;background:#fdeaea;color:#d84343" onclick="confirmarEliminar()">🗑 eliminar</button>
    <button class="cerrar" style="margin-right:.4rem;background:#E3EAF5;color:#26529E" onclick="abrirFormEditar()">✎ editar</button>
    <div class="foto-perfil">
      ${avatarHTML(c, true)}
      <button class="btn-foto" onclick="document.getElementById('foto-contacto-input').click()">📷 ${c.foto_url ? "Cambiar foto" : "Agregar foto"}</button>
      <input type="file" id="foto-contacto-input" accept="image/jpeg,image/png,image/webp" style="display:none"
             onchange="subirFotoContacto(this.files[0])">
    </div>
    <h2>${c.nombre}</h2>
    <div>
      ${c.relacion_tipo ? `<span class="chip ${c.relacion_tipo}">${c.relacion_tipo}</span>` : ""}
      ${c.relacion_estado ? `<span class="chip estado">${c.relacion_estado}</span>` : ""}
    </div>

    <div class="ventanas">
      <button class="ventana-btn v-info" onclick="cambiarVentana('info')">Información</button>
      <button class="ventana-btn v-notas" onclick="cambiarVentana('notas')">Anotaciones (${inter.length})</button>
      <button class="ventana-btn v-puntos" onclick="cambiarVentana('puntos')">Puntos a revisar (${totalPend - totalHechos})</button>
    </div>

    <div class="panel-ventana" id="pv-info">
      ${datosInfo.length
        ? datosInfo.map(d => `<div class="dato"><span class="etiqueta">${d[0]}</span><span class="valor">${d[1]}</span></div>`).join("")
        : "<div class='sin-datos'>Sin datos registrados</div>"}
      <div class="subtitulo">Reuniones (${reuniones.length})</div>
      ${reuniones.length ? reuniones.map(r => `
        <div class="dato">
          <span class="etiqueta">${r.inicio.slice(0,16)}</span>
          <span class="valor">${r.titulo}${r.ubicacion ? " · " + r.ubicacion : ""}</span>
        </div>`).join("") : "<div class='sin-datos'>Sin reuniones vinculadas — se sincroniza automáticamente</div>"}
    </div>

    <div class="panel-ventana" id="pv-notas">
      ${cajaVozFicha(`grabarParaContacto('${c.id}')`)}
      <div class="nota-form">
        <textarea id="texto-nota" placeholder="Escribe aquí lo que pasó: reunión, llamada, acuerdo, dato importante…"></textarea>
        <div class="fila-form">
          <select id="tipo-nota">
            <option value="nota">Nota</option>
            <option value="reunion">Reunión</option>
            <option value="llamada">Llamada</option>
            <option value="email">Email</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="otro">Otro</option>
          </select>
          <button class="btn-guardar" id="btn-nota" onclick="guardarNota()">Guardar</button>
        </div>
        <div class="aviso-ia" id="aviso-ia">✦ Claude está procesando la anotación…</div>
      </div>
      <div class="historial">
        ${inter.length ? inter.map(i => `
          <div class="inter" id="inter-${i.id}">
            <div class="inter-cabecera">
              <div class="fecha">${i.fecha.slice(0,16)} · ${i.tipo}</div>
              <div class="inter-acciones">
                <button class="btn-inter" onclick="abrirEditarAnotacion('${i.id}')">✎ Editar</button>
                <button class="btn-inter eliminar" onclick="eliminarAnotacion('${i.id}')">🗑 Borrar</button>
              </div>
            </div>
            <p>${i.resumen_ia || `<span class="sin-datos">procesando resumen…</span> ${i.contenido}`}</p>
          </div>`).join("") : "<div class='sin-datos'>Aún no hay conversaciones registradas</div>"}
      </div>
    </div>

    <div class="panel-ventana" id="pv-puntos">
      ${pendientesHtml || "<div class='sin-datos'>Nada pendiente por ahora</div>"}
    </div>
  `;
  cambiarVentana(ventanaInicial || "info");
}

async function guardarNota() {
  const texto = document.getElementById("texto-nota").value.trim();
  if (!texto) return;
  const tipo = document.getElementById("tipo-nota").value;
  document.getElementById("btn-nota").disabled = true;
  document.getElementById("aviso-ia").style.display = "block";
  await fetch("/interacciones", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ contacto_id: contactoAbierto, tipo: tipo, contenido_raw: texto }),
  });
  setTimeout(() => abrirFicha(contactoAbierto, "notas"), 6000);
}

function escaparHtml(texto) {
  return String(texto || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function abrirEditarAnotacion(interId) {
  const i = (window.interaccionesActuales || []).find(x => x.id === interId);
  const caja = document.getElementById("inter-" + interId);
  if (!i || !caja) return;
  const tipos = ["nota", "reunion", "llamada", "email", "whatsapp", "otro"];
  const opciones = tipos.map(t =>
    `<option value="${t}" ${i.tipo === t ? "selected" : ""}>${t.charAt(0).toUpperCase() + t.slice(1)}</option>`
  ).join("");
  caja.innerHTML = `
    <div class="fecha">Editando anotación</div>
    <div class="editor-nota">
      <textarea id="editar-texto-${interId}">${escaparHtml(i.contenido)}</textarea>
      <div class="editor-acciones">
        <select id="editar-tipo-${interId}">${opciones}</select>
        <button class="btn-guardar" onclick="guardarEdicionAnotacion('${interId}')">Guardar cambios</button>
        <button class="btn-inter" onclick="abrirFicha(contactoAbierto, 'notas')">Cancelar</button>
      </div>
      <div class="aviso-ia" id="editar-aviso-${interId}" style="display:none">✦ Claude está actualizando el resumen…</div>
    </div>`;
}

async function guardarEdicionAnotacion(interId) {
  const texto = document.getElementById("editar-texto-" + interId).value.trim();
  const tipo = document.getElementById("editar-tipo-" + interId).value;
  if (!texto) { alert("La anotación no puede quedar vacía."); return; }
  const aviso = document.getElementById("editar-aviso-" + interId);
  aviso.style.display = "block";
  const r = await fetch("/interacciones/" + interId, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tipo: tipo, contenido_raw: texto }),
  });
  if (!r.ok) {
    aviso.textContent = "No se pudo guardar la anotación.";
    return;
  }
  setTimeout(() => abrirFicha(contactoAbierto, "notas"), 1200);
}

async function eliminarAnotacion(interId) {
  if (!confirm("¿Eliminar esta anotación? Esta acción no se puede deshacer.")) return;
  const r = await fetch("/interacciones/" + interId, { method: "DELETE" });
  if (!r.ok) {
    alert("No se pudo eliminar la anotación.");
    return;
  }
  abrirFicha(contactoAbierto, "notas");
}

async function alternarTema(interId, indice, ev) {
  ev.stopPropagation();
  const el = ev.currentTarget;
  el.classList.toggle("hecho");
  el.classList.toggle("abierto");
  await fetch("/interacciones/" + interId + "/tema", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ indice: indice }),
  });
}

async function subirFotoContacto(archivo) {
  if (!archivo) return;
  if (archivo.size > 5_000_000) { alert("La imagen supera el máximo de 5 MB"); return; }
  const permitidos = ["image/jpeg", "image/png", "image/webp"];
  if (!permitidos.includes(archivo.type)) { alert("Usa una imagen JPG, PNG o WEBP"); return; }

  const form = new FormData();
  form.append("foto", archivo);
  const r = await fetch(`/contactos/${contactoAbierto}/foto`, { method: "POST", body: form });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    alert(err.detail || "No se pudo subir la foto");
    return;
  }
  await abrirFicha(contactoAbierto);
  await cargar();
}

async function abrirFormEditar() {
  const c = window.contactoActual;
  const empresas = await (await fetch("/empresas")).json();
  const opciones = empresas.map(e =>
    `<option value="${e.id}" ${c.empresa_id === e.id ? "selected" : ""}>${e.nombre}</option>`
  ).join("");
  const sel = v => c.relacion_tipo === v ? "selected" : "";
  ficha.innerHTML = `
    <button class="cerrar" onclick="abrirFicha(contactoAbierto)">← volver</button>
    <h2>Editar contacto</h2>
    <div style="margin-top:1.2rem">
      <div class="campo"><label>Nombre *</label><input type="text" id="f-nombre" value="${c.nombre || ""}"></div>
      <div class="dos-cols">
        <div class="campo"><label>Cargo</label><input type="text" id="f-cargo" value="${c.cargo || ""}"></div>
        <div class="campo"><label>Tipo de relación</label>
          <select id="f-tipo">
            <option value="">— elegir —</option>
            <option value="cliente" ${sel("cliente")}>Cliente</option>
            <option value="proveedor" ${sel("proveedor")}>Proveedor</option>
            <option value="socio" ${sel("socio")}>Socio</option>
            <option value="empresario" ${sel("empresario")}>Empresario</option>
            <option value="otro" ${sel("otro")}>Otro</option>
          </select>
        </div>
      </div>
      <div class="dos-cols">
        <div class="campo"><label>Empresa donde trabaja</label>
          <select id="f-empresa"><option value="">— sin empresa —</option>${opciones}</select>
        </div>
        <div class="campo"><label>Mi organización (contexto)</label>
          <select id="f-org">${opcionesOrganizacion(c.organizacion_id)}</select>
        </div>
      </div>
      <div class="campo"><label>Nicho</label><input type="text" id="f-nicho" value="${c.nicho || ""}"></div>
      <div class="dos-cols">
        <div class="campo"><label>Email</label><input type="text" id="f-email" value="${(c.emails || [])[0] || ""}"></div>
        <div class="campo"><label>Teléfono</label><input type="text" id="f-telefono" value="${c.telefono || ""}"></div>
      </div>
      <div class="campo"><label>LinkedIn</label><input type="text" id="f-linkedin" value="${c.linkedin_url || ""}"></div>
      <div class="campo"><label>Notas generales</label><textarea id="f-notas">${c.notas_generales || ""}</textarea></div>
      <button class="btn-guardar" id="btn-crear" onclick="guardarEdicion()">Guardar cambios</button>
      <div class="error-form" id="error-form"></div>
    </div>`;
}

async function guardarEdicion() {
  const nombre = val("f-nombre");
  if (!nombre) { mostrarError("El nombre es obligatorio"); return; }
  document.getElementById("btn-crear").disabled = true;
  const email = val("f-email");
  const r = await fetch("/contactos/" + contactoAbierto, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: nombre, cargo: val("f-cargo"), relacion_tipo: val("f-tipo"),
      empresa_id: val("f-empresa"), nicho: val("f-nicho"),
      organizacion_id: val("f-org"),
      telefono: val("f-telefono"), linkedin_url: val("f-linkedin"),
      notas_generales: val("f-notas"),
      emails: email ? [email] : [],
    }),
  });
  if (r.ok) { abrirFicha(contactoAbierto); cargarOrganizaciones(); cargar(); }
  else { mostrarError("No se pudo guardar"); document.getElementById("btn-crear").disabled = false; }
}

function confirmarEliminar() {
  const c = window.contactoActual;
  ficha.innerHTML = `
    <h2 style="color:#d84343">¿Eliminar a ${c.nombre}?</h2>
    <p style="margin-top:.9rem;font-size:.92rem;line-height:1.5">
      Esta acción <strong>no se puede deshacer</strong>. Se eliminará el contacto junto con
      <strong>todas sus anotaciones, resúmenes, puntos pendientes y vínculos con reuniones</strong>.
    </p>
    <div style="display:flex;gap:.6rem;margin-top:1.4rem">
      <button class="btn-guardar" style="background:#d84343" onclick="eliminarContacto()">Sí, eliminar todo</button>
      <button class="cerrar" style="float:none" onclick="abrirFicha(contactoAbierto)">Cancelar</button>
    </div>`;
}

async function eliminarContacto() {
  await fetch("/contactos/" + contactoAbierto, { method: "DELETE" });
  velo.classList.remove("abierto");
  cargar();
}

async function abrirFichaEmpresa(id) {
  empresaAbierta = id;
  ficha.innerHTML = "Cargando…";
  velo.classList.add("abierto");
  const e = await (await fetch("/empresas/" + id)).json();
  window.empresaActual = e;
  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
    <button class="cerrar" style="margin-right:.4rem;background:#fdeaea;color:#d84343" onclick="confirmarEliminarEmpresa()">🗑 eliminar</button>
    <button class="cerrar" style="margin-right:.4rem;background:#E3EAF5;color:#26529E" onclick="abrirFormEditarEmpresa()">✎ editar</button>
    <div class="foto-perfil">
      ${avatarHTML(e, true)}
      <button class="btn-foto" onclick="document.getElementById('foto-empresa-input').click()">📷 ${e.foto_url ? "Cambiar foto" : "Agregar foto"}</button>
      <input type="file" id="foto-empresa-input" accept="image/jpeg,image/png,image/webp" style="display:none"
             onchange="subirFotoEmpresa(this.files[0])">
    </div>
    <h2>${e.nombre}</h2>
    <div style="margin-top:1rem">
      ${cajaVozFicha(`grabarParaEmpresa('${e.id}')`)}
      ${[["Nicho", e.nicho], ["Mi organización", e.organizacion], ["Sitio web", e.sitio_web], ["Descripción", e.descripcion]]
        .filter(d => d[1])
        .map(d => `<div class="dato"><span class="etiqueta">${d[0]}</span><span class="valor">${d[1]}</span></div>`)
        .join("") || "<div class='sin-datos'>Sin datos adicionales</div>"}
    </div>`;
}

async function subirFotoEmpresa(archivo) {
  if (!archivo) return;
  if (archivo.size > 5_000_000) { alert("La imagen supera el máximo de 5 MB"); return; }
  const permitidos = ["image/jpeg", "image/png", "image/webp"];
  if (!permitidos.includes(archivo.type)) { alert("Usa una imagen JPG, PNG o WEBP"); return; }

  const form = new FormData();
  form.append("foto", archivo);
  const r = await fetch(`/empresas/${empresaAbierta}/foto`, { method: "POST", body: form });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    alert(err.detail || "No se pudo subir la foto");
    return;
  }
  await abrirFichaEmpresa(empresaAbierta);
  await cargar();
}

function abrirFormEditarEmpresa() {
  const e = window.empresaActual;
  ficha.innerHTML = `
    <button class="cerrar" onclick="abrirFichaEmpresa(empresaAbierta)">← volver</button>
    <h2>Editar empresa</h2>
    <div style="margin-top:1.2rem">
      <div class="campo"><label>Nombre *</label><input type="text" id="f-nombre" value="${e.nombre || ""}"></div>
      <div class="dos-cols">
        <div class="campo"><label>Nicho</label><input type="text" id="f-nicho" value="${e.nicho || ""}"></div>
        <div class="campo"><label>Sitio web</label><input type="text" id="f-web" value="${e.sitio_web || ""}"></div>
      </div>
      <div class="campo"><label>Mi organización (contexto)</label>
        <select id="f-org-emp">${opcionesOrganizacion(e.organizacion_id)}</select>
      </div>
      <div class="campo"><label>Descripción</label><textarea id="f-desc">${e.descripcion || ""}</textarea></div>
      <button class="btn-guardar" id="btn-crear" onclick="guardarEdicionEmpresa()">Guardar cambios</button>
      <div class="error-form" id="error-form"></div>
    </div>`;
}

async function guardarEdicionEmpresa() {
  const nombre = val("f-nombre");
  if (!nombre) { mostrarError("El nombre es obligatorio"); return; }
  document.getElementById("btn-crear").disabled = true;
  const r = await fetch("/empresas/" + empresaAbierta, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: nombre, nicho: val("f-nicho"),
      sitio_web: val("f-web"), descripcion: val("f-desc"),
      organizacion_id: val("f-org-emp"),
    }),
  });
  if (r.ok) { abrirFichaEmpresa(empresaAbierta); cargarOrganizaciones(); cargar(); }
  else { mostrarError("No se pudo guardar"); document.getElementById("btn-crear").disabled = false; }
}

function confirmarEliminarEmpresa() {
  const e = window.empresaActual;
  ficha.innerHTML = `
    <h2 style="color:#d84343">¿Eliminar ${e.nombre}?</h2>
    <p style="margin-top:.9rem;font-size:.92rem;line-height:1.5">
      Esta acción <strong>no se puede deshacer</strong>. Se eliminará la empresa y su información.
      Los contactos asociados <strong>no se eliminarán</strong> — solo quedarán sin empresa.
    </p>
    <div style="display:flex;gap:.6rem;margin-top:1.4rem">
      <button class="btn-guardar" style="background:#d84343" onclick="eliminarEmpresa()">Sí, eliminar</button>
      <button class="cerrar" style="float:none" onclick="abrirFichaEmpresa(empresaAbierta)">Cancelar</button>
    </div>`;
}

async function eliminarEmpresa() {
  await fetch("/empresas/" + empresaAbierta, { method: "DELETE" });
  velo.classList.remove("abierto");
  cargar();
}

async function cargarOrganizaciones() {
  try {
    misOrganizaciones = await (await fetch("/organizaciones")).json();
  } catch (e) { misOrganizaciones = []; }
  const sel = document.getElementById("filtro-org");
  const opciones = misOrganizaciones.map(o =>
    `<option value="${o.id}" ${filtroOrg === o.id ? "selected" : ""}>${o.nombre} (${o.contactos})</option>`
  ).join("");
  sel.innerHTML = `<option value="todas" ${filtroOrg === "todas" ? "selected" : ""}>Todas</option>`
    + opciones
    + `<option value="personal" ${filtroOrg === "personal" ? "selected" : ""}>Personal / sin organización</option>`;
}

function cambiarFiltroOrg(valor) {
  filtroOrg = valor;
  localStorage_seguro("il_filtro_org", valor);
  marcarFiltroActivo();
  cargar();
}

function marcarFiltroActivo() {
  const sel = document.getElementById("filtro-org");
  if (sel) sel.classList.toggle("activo", filtroOrg !== "todas");
}

function alternarMenuUsuario(ev) {
  ev.stopPropagation();
  document.getElementById("menu-usuario").classList.toggle("abierto");
}

function cerrarMenuUsuario() {
  const m = document.getElementById("menu-usuario");
  if (m) m.classList.remove("abierto");
}

document.addEventListener("click", cerrarMenuUsuario);

function grabarRapido() {
  destinoVoz = null;
  irAVista("importar");
  setTimeout(() => {
    const btn = document.getElementById("btn-grabar");
    if (btn) btn.scrollIntoView({ behavior: "smooth", block: "center" });
  }, 250);
}

function diasDesde(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  return Math.floor((Date.now() - d.getTime()) / 86400000);
}

function textoUltimoContacto(iso) {
  const dias = diasDesde(iso);
  if (dias === null) return "sin contacto aún";
  if (dias === 0) return "hoy";
  if (dias === 1) return "ayer";
  if (dias < 30) return "hace " + dias + " días";
  const meses = Math.floor(dias / 30);
  return "hace " + meses + (meses === 1 ? " mes" : " meses");
}

async function cargarHoy() {
  contenido.innerHTML = "<div class='vacio'>Cargando tu día…</div>";
  const d = await (await fetch("/hoy?org=" + filtroOrg)).json();
  const ahora = new Date();
  const hoyStr = ahora.toDateString();
  const deHoy = d.eventos.filter(e => new Date(e.inicio).toDateString() === hoyStr);

  const pintarEvento = e => {
    const f = new Date(e.inicio);
    const h = (f.getHours() === 0 && f.getMinutes() === 0)
      ? "todo el día"
      : String(f.getHours()).padStart(2,"0") + ":" + String(f.getMinutes()).padStart(2,"0");
    const gente = (e.asistentes || []).filter(a => a.nombre);
    return `<div class="hoy-evento" onclick="irAAgenda()">
      <div class="hora-grande">${h}</div>
      <div style="flex:1">
        <h4>${e.titulo}</h4>
        ${e.ubicacion ? `<div class="meta">📍 ${e.ubicacion}</div>` : ""}
        ${gente.length ? `<div class="meta" style="margin-top:.3rem">Con: ${gente.map(a =>
          a.contacto_id
            ? `<span style="color:#26529E;font-weight:700;cursor:pointer" onclick="event.stopPropagation();abrirFicha('${a.contacto_id}')">${a.nombre}</span>`
            : a.nombre).join(", ")}</div>` : ""}
      </div>
    </div>`;
  };

  let html = `
    <div id="caja-brief"></div>

    <div class="hoy-seccion">
      <div class="hoy-titulo">Agenda de hoy</div>
      ${deHoy.length ? deHoy.map(pintarEvento).join("")
        : "<div class='hoy-vacio'>No tienes eventos agendados para hoy</div>"}
    </div>

    <div class="hoy-seccion">
      <div class="hoy-titulo plegable" onclick="alternarPendientes()">
        <span class="flecha-pleg" id="flecha-pend">▶</span>
        ☐ Pendientes abiertos
        <span class="conteo-pleg ${d.total_pendientes ? "" : "cero"}">${d.total_pendientes}</span>
      </div>
      <div id="lista-pendientes">
        ${d.pendientes.length ? d.pendientes.map(p => `
          <div class="hoy-pend" onclick="abrirFicha('${p.contacto_id}','puntos')">
            <div style="flex:1">
              <div class="quien">${p.contacto}${p.empresa ? " · " + p.empresa : ""}</div>
              <div class="que">${p.texto}</div>
              <div class="detalle-pend">Registrado ${textoUltimoContacto(p.fecha)}</div>
            </div>
          </div>`).join("")
          : "<div class='hoy-vacio'>Nada pendiente. Todo al día 👌</div>"}
        ${d.total_pendientes > d.pendientes.length
          ? `<div class="hoy-vacio">Mostrando ${d.pendientes.length} de ${d.total_pendientes}. Ve a la pestaña Tareas para verlos todos.</div>`
          : ""}
      </div>
    </div>`;

  contenido.innerHTML = html;
  cargarBrief();
}

async function cargarBrief() {
  const caja = document.getElementById("caja-brief");
  if (!caja) return;
  let b;
  try {
    b = await (await fetch("/brief")).json();
  } catch (e) { return; }

  if (!b.existe) {
    caja.innerHTML = `
      <div class="brief">
        <div class="brief-cabecera">
          <div>
            <div class="brief-marca">Brief matutino</div>
            <h3>Aún no se ha generado el brief de hoy</h3>
            <div class="meta" style="margin-top:.3rem">Se genera solo cada mañana a las 6:00. Puedes pedirlo ahora.</div>
          </div>
          <button class="btn-brief" id="btn-brief" onclick="generarBrief()">Generar ahora</button>
        </div>
      </div>`;
    return;
  }
  pintarBrief(b);
}

function pintarBrief(b) {
  const caja = document.getElementById("caja-brief");
  if (!caja) return;
  const hora = b.generado_en ? b.generado_en.slice(11, 16) : "";
  caja.innerHTML = `
    <div class="brief">
      <div class="brief-cabecera">
        <div>
          <div class="brief-marca">Brief matutino</div>
          <h3>${b.saludo || ""}</h3>
          <div class="meta">${b.fecha_texto || ""}</div>
        </div>
        <button class="btn-brief secundario" id="btn-brief" onclick="generarBrief()">↻ Actualizar</button>
      </div>

      ${b.resumen ? `<div class="resumen">${b.resumen}</div>` : ""}

      ${(b.puntos_clave || []).length ? `
        <div class="brief-bloque">
          <h5>No puedes olvidar</h5>
          ${b.puntos_clave.map(p => `<div class="brief-punto">${p}</div>`).join("")}
        </div>` : ""}

      <div class="brief-pie">Generado por Claude${hora ? " a las " + hora : ""} · ${b.total_eventos || 0} evento(s), ${b.total_pendientes || 0} pendiente(s)</div>
    </div>`;
}

async function generarBrief() {
  const btn = document.getElementById("btn-brief");
  if (btn) { btn.disabled = true; btn.textContent = "✦ Escribiendo…"; }
  try {
    const r = await fetch("/brief/generar", { method: "POST" });
    if (!r.ok) throw new Error("fallo");
    const b = await r.json();
    b.existe = true;
    b.generado_en = new Date().toISOString();
    pintarBrief(b);
  } catch (e) {
    if (btn) { btn.disabled = false; btn.textContent = "Reintentar"; }
    const caja = document.getElementById("caja-brief");
    if (caja) caja.insertAdjacentHTML("beforeend",
      "<div class='msj-importar mal' style='display:block;margin-top:.5rem'>No se pudo generar el brief. Revisa la conexión o el crédito de la API.</div>");
  }
}

function alternarPendientes() {
  const lista = document.getElementById("lista-pendientes");
  const flecha = document.getElementById("flecha-pend");
  if (!lista) return;
  const abierta = lista.classList.toggle("abierta");
  if (flecha) flecha.classList.toggle("abierta", abierta);
}

function irAAgenda() {
  irAVista("agenda");
}

function opcionesOrganizacion(seleccionada) {
  return `<option value="">— sin organización —</option>` + misOrganizaciones.map(o =>
    `<option value="${o.id}" ${seleccionada === o.id ? "selected" : ""}>${o.nombre}</option>`
  ).join("");
}

async function cargarTareas() {
  contenido.innerHTML = "<div class='vacio'>Cargando tareas…</div>";
  const d = await (await fetch("/organizaciones/tareas?org=" + filtroOrg)).json();
  contenido.innerHTML = "";

  const kpis = document.createElement("div");
  kpis.className = "contador-org";
  kpis.innerHTML = `
    <div class="kpi"><div class="num">${d.pendientes}</div><div class="lbl">Pendientes</div></div>
    <div class="kpi"><div class="num">${d.total - d.pendientes}</div><div class="lbl">Completadas</div></div>
    <div class="kpi"><div class="num">${d.total}</div><div class="lbl">Total</div></div>`;
  contenido.appendChild(kpis);

  if (!d.tareas.length) {
    const v = document.createElement("div");
    v.className = "vacio";
    v.textContent = "No hay tareas registradas en este filtro";
    contenido.appendChild(v);
    return;
  }

  const porPersona = {};
  d.tareas.forEach(t => {
    if (!porPersona[t.contacto_id]) porPersona[t.contacto_id] = { info: t, lista: [] };
    porPersona[t.contacto_id].lista.push(t);
  });

  Object.values(porPersona).forEach(g => {
    const bloque = document.createElement("div");
    bloque.className = "tarea-grupo";
    const abiertas = g.lista.filter(t => !t.hecho).length;
    const detalle = [g.info.cargo, g.info.empresa].filter(Boolean).join(" · ");
    bloque.innerHTML = `
      <div class="tarea-persona">
        ${avatarHTML(g.info)}
        <div>
          <span class="nom" onclick="abrirFicha('${g.info.contacto_id}')">${g.info.contacto}</span>
          ${g.info.organizacion ? `<span class="chip org">${g.info.organizacion}</span>` : ""}
          <div class="emp">${detalle}${detalle ? " · " : ""}${abiertas} pendiente(s)</div>
        </div>
      </div>
      ${g.lista.map(t => `<div class="pendiente ${t.hecho ? "hecho" : "abierto"}"
        onclick="alternarTemaLista('${t.interaccion_id}', ${t.indice}, event)"><span>${t.texto}</span>
        <button class="btn-borrar-mini borrar-tema" title="Eliminar punto"
          onclick="eliminarTema('${t.interaccion_id}', ${t.indice}, event)">🗑</button></div>`).join("")}`;
    contenido.appendChild(bloque);
  });
}

async function eliminarTema(interId, indice, ev) {
  ev.stopPropagation();
  if (!confirm("¿Eliminar este punto pendiente? La anotación original se conserva.")) return;
  await fetch("/interacciones/" + interId + "/tema/" + indice, { method: "DELETE" });
  if (vista === "tareas") cargarTareas();
  else if (contactoAbierto) abrirFicha(contactoAbierto, "puntos");
}

async function abrirConfiguracion() {
  velo.classList.add("abierto");
  ficha.innerHTML = "Cargando…";
  const p = await (await fetch("/perfil")).json();
  await cargarOrganizaciones();
  const s = p.estadisticas || {};
  const orgs = misOrganizaciones.length
    ? misOrganizaciones.map(o => `
        <div class="org-item">
          <div class="datos">
            <div class="nom">${o.nombre}</div>
            <div class="meta2">${o.mi_cargo || "sin cargo definido"} · ${o.contactos} contacto(s)</div>
          </div>
          <button class="btn-mini rojo" onclick="eliminarOrganizacionConfig('${o.id}', '${o.nombre.replace(/'/g, "")}')">Eliminar</button>
        </div>`).join("")
    : "<div class='sin-datos'>Aún no has agregado organizaciones</div>";

  ficha.innerHTML = `
    <button class="cerrar" onclick="velo.classList.remove('abierto')">✕ cerrar</button>
    <h2>Configuración de usuario</h2>
    <div class="meta" style="margin-top:.3rem">Usuario: @${p.username}</div>

    <div class="kpi-perfil">
      <div class="kpi"><div class="num">${s.contactos || 0}</div><div class="lbl">Contactos</div></div>
      <div class="kpi"><div class="num">${s.empresas || 0}</div><div class="lbl">Empresas</div></div>
      <div class="kpi"><div class="num">${s.anotaciones || 0}</div><div class="lbl">Notas</div></div>
      <div class="kpi"><div class="num">${s.organizaciones || 0}</div><div class="lbl">Organiz.</div></div>
    </div>

    <div class="subtitulo">Mis datos</div>
    <div class="campo"><label>Nombre visible</label>
      <input type="text" id="p-nombre" value="${p.nombre_visible || ""}" placeholder="Ej: Rodrigo Oryan"></div>
    <div class="dos-cols">
      <div class="campo"><label>Email</label>
        <input type="text" id="p-email" value="${p.email || ""}" placeholder="rodrigo@empresa.cl"></div>
      <div class="campo"><label>Telefono</label>
        <input type="text" id="p-telefono" value="${p.telefono || ""}" placeholder="+56 9 ..."></div>
    </div>
    <button class="btn-guardar" id="btn-perfil" onclick="guardarPerfil()">Guardar mis datos</button>
    <span id="msj-perfil" class="msj-importar" style="margin-left:.7rem"></span>

    <div class="subtitulo" style="margin-top:1.6rem">Mis organizaciones</div>
    <div class="meta" style="margin-bottom:.7rem">Los lugares donde trabajas. Cada contacto puede asociarse a una de ellas.</div>
    ${orgs}
    <div style="margin-top:1rem;border-top:1px solid #EEEEEE;padding-top:1rem">
      <button class="btn-guardar" id="btn-abrir-org" onclick="mostrarFormOrg()">+ Agregar organización</button>
      <div id="form-org" style="display:none;margin-top:1rem">
        <div class="dos-cols">
          <div class="campo"><label>Nombre de la organización *</label>
            <input type="text" id="o-nombre" placeholder="Ej: John Oryan Surveyors"></div>
          <div class="campo"><label>Mi cargo ahí</label>
            <input type="text" id="o-cargo" placeholder="Ej: Gerente General"></div>
        </div>
        <button class="btn-guardar" id="btn-org" onclick="crearOrganizacionConfig()">Guardar organización</button>
        <button class="cerrar" style="float:none;margin-left:.5rem" onclick="ocultarFormOrg()">Cancelar</button>
        <div class="error-form" id="error-form"></div>
      </div>
    </div>`;
}

function mostrarFormOrg() {
  document.getElementById("btn-abrir-org").style.display = "none";
  document.getElementById("form-org").style.display = "block";
  document.getElementById("o-nombre").focus();
}

function ocultarFormOrg() {
  document.getElementById("form-org").style.display = "none";
  document.getElementById("btn-abrir-org").style.display = "";
  document.getElementById("o-nombre").value = "";
  document.getElementById("o-cargo").value = "";
  document.getElementById("error-form").style.display = "none";
}

async function guardarPerfil() {
  const btn = document.getElementById("btn-perfil");
  const msj = document.getElementById("msj-perfil");
  btn.disabled = true;
  const r = await fetch("/perfil", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre_visible: val("p-nombre"),
      email: val("p-email"),
      telefono: val("p-telefono"),
    }),
  });
  msj.className = "msj-importar " + (r.ok ? "ok" : "mal");
  msj.textContent = r.ok ? "Guardado" : "No se pudo guardar";
  btn.disabled = false;
  if (r.ok) mostrarUsuario();
}

async function crearOrganizacionConfig() {
  const nombre = val("o-nombre");
  if (!nombre) { mostrarError("El nombre es obligatorio"); return; }
  document.getElementById("btn-org").disabled = true;
  const r = await fetch("/organizaciones", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre: nombre, mi_cargo: val("o-cargo") }),
  });
  if (r.ok) { await abrirConfiguracion(); cargar(); }
  else { mostrarError("No se pudo crear"); document.getElementById("btn-org").disabled = false; }
}

async function eliminarOrganizacionConfig(id, nombre) {
  if (!confirm("Eliminar " + nombre + "? Sus contactos NO se borran, solo quedan sin organización.")) return;
  await fetch("/organizaciones/" + id, { method: "DELETE" });
  if (filtroOrg === id) filtroOrg = "todas";
  await abrirConfiguracion();
  cargar();
}

async function alternarTemaLista(interId, indice, ev) {
  ev.stopPropagation();
  const el = ev.currentTarget;
  el.classList.toggle("hecho");
  el.classList.toggle("abierto");
  await fetch("/interacciones/" + interId + "/tema", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ indice: indice }),
  });
}

cargarOrganizaciones().then(() => { marcarFiltroActivo(); irAVista("hoy"); });
function cerrarSesion() {
  if (confirm("¿Cerrar sesión?")) window.location.href = "/salir";
}
async function mostrarUsuario() {
  try {
    const r = await fetch("/quien-soy");
    const d = await r.json();
    if (d.usuario) {
      let etiqueta = "@" + d.usuario;
      try {
        const p = await (await fetch("/perfil")).json();
        if (p.nombre_visible) { etiqueta = p.nombre_visible; window.perfilNombre = p.nombre_visible; }
      } catch (e2) {}
      document.getElementById("nombre-usuario").textContent = etiqueta;
    }
  } catch (e) {}
}
mostrarUsuario();
</script>
</body>
</html>"""


@router.get("/panel", response_class=HTMLResponse)
def panel():
    return PAGINA