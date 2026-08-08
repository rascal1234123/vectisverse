window.RIPTIDE_HQ_TOUR = {
  startNode: '01',
  yaw: { seaward: 0, upperWall: 90, landward: 180, lowerWall: 270 },
  pitchLimits: [-55, 55],
  defaultPitch: 0,
  defaultFov: 75,
  nodes: [
    { id:'01', quarter:'Q2', label:'Team Area', image:'assets/riptide-hq/node-01-production-beta.webp?v=4a4', mobile:'assets/riptide-hq/node-01-production-beta.webp?v=4a4', previous:null, next:'02' },
    { id:'02', quarter:'Q2', label:'Team / Training Transition', image:'assets/riptide-hq/hq-node-02-beta.svg?v=beta1', mobile:'assets/riptide-hq/hq-node-02-beta.svg?v=beta1', previous:'01', next:'03' },
    { id:'03', quarter:'Q3', label:'Training Area', image:'assets/riptide-hq/hq-node-03-beta.svg?v=beta1', mobile:'assets/riptide-hq/hq-node-03-beta.svg?v=beta1', previous:'02', next:'04' },
    { id:'04', quarter:'Q3', label:'Training / Briefing Transition', image:'assets/riptide-hq/hq-node-04-beta.svg?v=beta1', mobile:'assets/riptide-hq/hq-node-04-beta.svg?v=beta1', previous:'03', next:'05' },
    { id:'05', quarter:'Q4', label:'Briefing Area', image:'assets/riptide-hq/hq-node-05-beta.svg?v=beta1', mobile:'assets/riptide-hq/hq-node-05-beta.svg?v=beta1', previous:'04', next:null }
  ]
};
