
var wristSphereGeometry = new THREE.SphereGeometry(10,36,16)
var tipSphereGeometry = new THREE.SphereGeometry(8	,36,16)
var sphereMaterial = new THREE.MeshLambertMaterial({ color:0xff0000 })

var cylinderMaterial = new THREE.MeshNormalMaterial({color : 0xcccccc})

var cylinderGeometry  = new THREE.CylinderGeometry(5,1,200,10)	

cylinderGeometry.applyMatrix( new THREE.Matrix4().makeRotationX( - Math.PI / 2 ) ); 