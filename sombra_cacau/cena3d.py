from pathlib import Path

_PASTA_ESTATICA = Path(__file__).parent / "static"
_THREE_JS = (_PASTA_ESTATICA / "three.min.js").read_text(encoding="utf-8")
_ORBIT_CONTROLS_JS = (_PASTA_ESTATICA / "OrbitControls.js").read_text(encoding="utf-8")

TEMPLATE_HTML = """
<div id="cena3d" style="width:100%; height:600px; border-radius:12px; overflow:hidden;"></div>
<script>__THREE_JS__</script>
<script>__ORBIT_CONTROLS_JS__</script>
<script>
(function() {
  const altura = __ALTURA__;
  const raioCopa = __RAIO_COPA__;
  const direcaoSombra = __DIRECAO_SOMBRA__ * Math.PI / 180;
  const elevacaoSolar = __ELEVACAO_SOLAR__ * Math.PI / 180;
  const azimuteSolar = __AZIMUTE_SOLAR__ * Math.PI / 180;

  const container = document.getElementById('cena3d');
  const largura = container.clientWidth;
  const alturaTela = 600;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xCFE0EC);
  scene.fog = new THREE.Fog(0xCFE0EC, 20, 45);

  const camera = new THREE.PerspectiveCamera(45, largura / alturaTela, 0.1, 1000);
  camera.position.set(12, 9, 12);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(largura, alturaTela);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.target.set(0, altura / 3, 0);
  controls.update();

  // ---------- Luz ----------
  scene.add(new THREE.HemisphereLight(0xCFE0EC, 0x8FA876, 0.55));

  const distanciaSol = 18;
  const distHorizontal = distanciaSol * Math.cos(elevacaoSolar);
  const sunX = distHorizontal * Math.sin(azimuteSolar);
  const sunZ = -distHorizontal * Math.cos(azimuteSolar);
  const sunY = distanciaSol * Math.sin(elevacaoSolar);

  const luzSol = new THREE.DirectionalLight(0xfff2d0, 1.15);
  luzSol.position.set(sunX, sunY, sunZ);
  luzSol.castShadow = true;
  luzSol.shadow.mapSize.width = 1536;
  luzSol.shadow.mapSize.height = 1536;
  luzSol.shadow.camera.left = -12;
  luzSol.shadow.camera.right = 12;
  luzSol.shadow.camera.top = 12;
  luzSol.shadow.camera.bottom = -12;
  luzSol.shadow.camera.near = 0.5;
  luzSol.shadow.camera.far = 40;
  luzSol.shadow.bias = -0.001;
  scene.add(luzSol);

  // Sol visível, com halo, para não ser confundido com a bússola
  const grupoSol = new THREE.Group();
  const sol = new THREE.Mesh(
    new THREE.SphereGeometry(0.45, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xFFD24A })
  );
  grupoSol.add(sol);
  const halo = new THREE.Mesh(
    new THREE.SphereGeometry(0.75, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0xFFE9A8, transparent: true, opacity: 0.35 })
  );
  grupoSol.add(halo);
  grupoSol.position.set(sunX, Math.max(sunY, 0.6), sunZ);
  scene.add(grupoSol);

  function criarRotuloTexto(texto, cor) {
    const canvas = document.createElement('canvas');
    canvas.width = 128; canvas.height = 128;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = cor;
    ctx.font = 'bold 72px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(texto, 64, 64);
    const tex = new THREE.CanvasTexture(canvas);
    return new THREE.SpriteMaterial({ map: tex, transparent: true });
  }

  const rotuloSol = new THREE.Sprite(criarRotuloTexto('Sol', '#B8860B'));
  rotuloSol.scale.set(1.4, 1.4, 1);
  rotuloSol.position.set(sunX, Math.max(sunY, 0.6) + 1.1, sunZ);
  scene.add(rotuloSol);

  // ---------- Chão com textura de grama ----------
    function criarTexturaGrama() {
    const canvas = document.createElement('canvas');
    canvas.width = 256; canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#8FA876';
    ctx.fillRect(0, 0, 256, 256);
    const tons = ['rgba(120,150,95,0.4)', 'rgba(140,170,110,0.35)', 'rgba(100,130,80,0.4)'];
    for (let i = 0; i < 900; i++) {
      ctx.strokeStyle = tons[i % tons.length];
      ctx.lineWidth = 1;
      const x = Math.random() * 256;
      const y = Math.random() * 256;
      const comprimento = 3 + Math.random() * 5;
      const angulo = Math.random() * Math.PI * 2;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + Math.cos(angulo) * comprimento, y + Math.sin(angulo) * comprimento);
      ctx.stroke();
    }
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    return tex;
  }
  const texturaGrama = criarTexturaGrama();

  const chao = new THREE.Mesh(
    new THREE.CircleGeometry(11, 64),
    new THREE.MeshStandardMaterial({ map: texturaGrama, roughness: 1 })
  );
  chao.rotation.x = -Math.PI / 2;
  chao.receiveShadow = true;
  scene.add(chao);

  // ---------- Bússola discreta (anel + letras) ----------
  const anelBussola = new THREE.Mesh(
    new THREE.RingGeometry(9.7, 9.85, 64),
    new THREE.MeshBasicMaterial({ color: 0x3D2B1F, side: THREE.DoubleSide, transparent: true, opacity: 0.55 })
  );
  anelBussola.rotation.x = -Math.PI / 2;
  anelBussola.position.y = 0.015;
  scene.add(anelBussola);

  function criarRotuloBussola(texto, x, z) {
    const sprite = new THREE.Sprite(criarRotuloTexto(texto, '#3D2B1F'));
    sprite.scale.set(0.9, 0.9, 1);
    sprite.position.set(x, 0.4, z);
    scene.add(sprite);
  }
  criarRotuloBussola('N', 0, -9.8);
  criarRotuloBussola('S', 0, 9.8);
  criarRotuloBussola('L', 9.8, 0);
  criarRotuloBussola('O', -9.8, 0);

  // ---------- Árvore ----------
  const grupoArvore = new THREE.Group();

  const tronco = new THREE.Mesh(
    new THREE.CylinderGeometry(0.11, 0.18, altura * 0.6, 10),
    new THREE.MeshStandardMaterial({ color: 0x5C3A21, roughness: 0.95 })
  );
  tronco.position.y = (altura * 0.6) / 2;
  tronco.castShadow = true;
  grupoArvore.add(tronco);

  // Copa orgânica: vários aglomerados irregulares em vez de uma esfera perfeita
  const alturaBaseCopa = altura * 0.6;
  const coresCopa = [0x2E7D45, 0x358A4E, 0x276B3C, 0x3D9457];
  const numAglomerados = 7;
  for (let i = 0; i < numAglomerados; i++) {
    const anguloAleatorio = Math.random() * Math.PI * 2;
    const distanciaAleatoria = Math.random() * raioCopa * 0.55;
    const tamanho = raioCopa * (0.55 + Math.random() * 0.4);

    const aglomerado = new THREE.Mesh(
      new THREE.IcosahedronGeometry(tamanho, 1),
      new THREE.MeshStandardMaterial({
        color: coresCopa[i % coresCopa.length],
        roughness: 0.85,
        flatShading: true
      })
    );
    aglomerado.position.set(
      Math.cos(anguloAleatorio) * distanciaAleatoria,
      alturaBaseCopa + raioCopa * 0.55 + (Math.random() - 0.5) * raioCopa * 0.4,
      Math.sin(anguloAleatorio) * distanciaAleatoria
    );
    aglomerado.castShadow = true;
    grupoArvore.add(aglomerado);
  }

  scene.add(grupoArvore);

  // ---------- Silhueta humana (1,70 m, referência de escala) ----------
  const grupoPessoa = new THREE.Group();
  const corpo = new THREE.Mesh(
    new THREE.CylinderGeometry(0.2, 0.22, 1.3, 12),
    new THREE.MeshStandardMaterial({ color: 0x4A4A4A, roughness: 0.9 })
  );
  corpo.position.y = 1.3 / 2 + 0.2;
  corpo.castShadow = true;
  grupoPessoa.add(corpo);

  const cabeca = new THREE.Mesh(
    new THREE.SphereGeometry(0.17, 14, 14),
    new THREE.MeshStandardMaterial({ color: 0x4A4A4A, roughness: 0.9 })
  );
  cabeca.position.y = 1.3 + 0.2 + 0.17;
  cabeca.castShadow = true;
  grupoPessoa.add(cabeca);

  grupoPessoa.position.set(raioCopa + 1.7, 0, 0);
  scene.add(grupoPessoa);

  function animar() {
    requestAnimationFrame(animar);
    controls.update();
    renderer.render(scene, camera);
  }
  animar();
})();
</script>
"""


def gerar_cena_3d(altura, raio_copa, comprimento_sombra, direcao_sombra, elevacao_solar, azimute_solar):
    """
    Gera o HTML/JS (Three.js) de uma cena 3D ilustrativa: árvore de cacau
    com copa orgânica (múltiplos aglomerados irregulares), sombra real
    calculada pelo motor 3D via shadow mapping (luz direcional posicionada
    na elevação/azimute solar reais), bússola discreta (N/S/L/O), sol
    destacado com halo e rótulo, e uma silhueta humana de 1,70 m como
    referência de escala.

    A sombra não é mais desenhada manualmente como uma elipse: ela é
    o resultado real do cálculo de sombreamento do motor gráfico,
    a partir da mesma posição solar (elevação/azimute) usada nos
    cálculos numéricos do restante do software — os dois devem ser
    consistentes entre si.

    O parâmetro comprimento_sombra é mantido na assinatura por
    compatibilidade, mas não é mais usado diretamente na cena.
    """
    html = TEMPLATE_HTML
    html = html.replace("__ALTURA__", str(altura))
    html = html.replace("__RAIO_COPA__", str(raio_copa))
    html = html.replace("__DIRECAO_SOMBRA__", str(direcao_sombra))
    html = html.replace("__ELEVACAO_SOLAR__", str(elevacao_solar))
    html = html.replace("__AZIMUTE_SOLAR__", str(azimute_solar))
    html = html.replace("__THREE_JS__", _THREE_JS)
    html = html.replace("__ORBIT_CONTROLS_JS__", _ORBIT_CONTROLS_JS)
    return html