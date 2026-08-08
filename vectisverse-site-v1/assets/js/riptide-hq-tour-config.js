window.RIPTIDE_HQ_TOUR = {
  startNode: '01',
  yaw: { seaward: 0, upperWall: 90, landward: 180, lowerWall: 270 },
  pitchLimits: [-55, 55],
  defaultPitch: 0,
  defaultFov: 75,
  nodes: [
    { id:'01', quarter:'Q2', label:'Team Area', image:'hq-node-01-clean-v13.svg', mobile:'hq-node-01-clean-v13.svg', previous:null, next:'02' },
    { id:'02', quarter:'Q2', label:'Team / Training Transition', image:'hq-node-02-diag.svg', mobile:'hq-node-02-diag.svg', previous:'01', next:'03' },
    { id:'03', quarter:'Q3', label:'Training Area', image:'hq-node-03-diag.svg', mobile:'hq-node-03-diag.svg', previous:'02', next:'04' },
    { id:'04', quarter:'Q3', label:'Training / Briefing Transition', image:'hq-node-04-diag.svg', mobile:'hq-node-04-diag.svg', previous:'03', next:'05' },
    { id:'05', quarter:'Q4', label:'Briefing Area', image:'hq-node-05-diag.svg', mobile:'hq-node-05-diag.svg', previous:'04', next:null }
  ]
};
