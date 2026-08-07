window.RIPTIDE_HQ_TOUR = {
  startNode: '01',
  yaw: { seaward: 0, upperWall: 90, landward: 180, lowerWall: 270 },
  pitchLimits: [-55, 55],
  defaultPitch: 0,
  defaultFov: 75,
  nodes: [
    { id:'01', quarter:'Q2', label:'Team Area', image:'assets/riptide/hq-tour/node-01/node-01-1024.webp', mobile:'assets/riptide/hq-tour/node-01/node-01-1024.webp', previous:null, next:'02' },
    { id:'02', quarter:'Q2', label:'Team / Training Transition', image:'assets/riptide/hq-tour/node-02/node-02-2560.webp', mobile:'assets/riptide/hq-tour/node-02/node-02-2560.webp', previous:'01', next:'03' },
    { id:'03', quarter:'Q3', label:'Training Area', image:'assets/riptide/hq-tour/node-03/node-03-2560.webp', mobile:'assets/riptide/hq-tour/node-03/node-03-2560.webp', previous:'02', next:'04' },
    { id:'04', quarter:'Q3', label:'Training / Briefing Transition', image:'assets/riptide/hq-tour/node-04/node-04-2560.webp', mobile:'assets/riptide/hq-tour/node-04/node-04-2560.webp', previous:'03', next:'05' },
    { id:'05', quarter:'Q4', label:'Briefing Area', image:'assets/riptide/hq-tour/node-05/node-05-2560.webp', mobile:'assets/riptide/hq-tour/node-05/node-05-2560.webp', previous:'04', next:null }
  ]
};
