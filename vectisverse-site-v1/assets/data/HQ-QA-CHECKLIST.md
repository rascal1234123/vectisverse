# RIPTIDE HQ — QA CHECKLIST

Version: 1.0
Status: ACTIVE

A release candidate is PASS only when every applicable item below passes against the same build.

## 1. Authority / topology
- [ ] Build uses current authoritative geometry master.
- [ ] Q1/Q2 partition/access preserved.
- [ ] Q2/Q3 open; no wall or door.
- [ ] Q3/Q4 open; no wall or door.
- [ ] Continuous Q2→Q3→Q4 longitudinal relationship preserved.
- [ ] Q3 equipment remains in Q3.
- [ ] Q4 briefing elements remain in Q4.
- [ ] Exactly one Q4 seaward circular window.

## 2. Camera / projection
- [ ] Nodes 01–05 occupy the approved shared coordinate system.
- [ ] Node order is 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05.
- [ ] Eye height and camera positions match the geometry master.
- [ ] 0° yaw = seaward for every node.
- [ ] Every final panorama is exactly 2:1 equirectangular.
- [ ] No upside-down projection or vertical inversion.

## 3. Panorama integrity
- [ ] No duplicated panorama strips.
- [ ] No blank/solid hemispheres.
- [ ] No visible seam discontinuity in normal viewing.
- [ ] Floor, wall and ceiling geometry is continuous.
- [ ] No ghosted or duplicated objects.
- [ ] No unintended geometry.
- [ ] No non-authoritative object addition, removal or repositioning.
- [ ] Lighting/material continuity is acceptable between adjacent nodes.

## 4. Delivery assets
- [ ] Node 01 release WebP present.
- [ ] Node 02 release WebP present.
- [ ] Node 03 release WebP present.
- [ ] Node 04 release WebP present.
- [ ] Node 05 release WebP present.
- [ ] Desktop derivatives are 4096×2048 where approved source quality supports them.
- [ ] Mobile derivatives are 2048×1024.
- [ ] Assets decode successfully in browser.
- [ ] Asset URLs return correct MIME type and no unexpected redirects/errors.

## 5. Pannellum / interaction
- [ ] Pannellum starts successfully.
- [ ] Node 01 loads as start scene.
- [ ] Forward navigation works 01→02→03→04→05.
- [ ] Back navigation works 05→04→03→02→01.
- [ ] Drag/touch look-around works.
- [ ] Limited zoom works.
- [ ] Pitch limits are enforced.
- [ ] Return to Start works.
- [ ] Exit Tour works.
- [ ] Keyboard controls work.
- [ ] Reduced-motion path avoids unnecessary transition animation.
- [ ] Loading/error state is accessible and non-blocking.

## 6. Regression / browsers
- [ ] Current Safari desktop PASS.
- [ ] Current Chrome desktop PASS.
- [ ] Current Firefox desktop PASS.
- [ ] Current Edge desktop PASS.
- [ ] Current iPhone Safari PASS.
- [ ] Portrait and landscape mobile layouts PASS.
- [ ] No console errors affecting core use.
- [ ] No unacceptable memory/performance regression across all five nodes.

## 7. Deployment
- [ ] Final config references only release assets.
- [ ] Cache-bust versions match final deployment.
- [ ] Production URL loads from a clean/private session.
- [ ] All five nodes load from production, not local/staging cache.
- [ ] Production smoke test passes forward and reverse navigation.
- [ ] Last-known-good rollback point recorded.

Release status: FAIL until every required checkbox is verified against the same production candidate.