import { createHash } from 'node:crypto';
import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const ROOT = process.cwd();
const SOURCE_ROOT = path.resolve(ROOT, 'asset-source');
const OUTPUT_ROOT = path.resolve(ROOT, 'vectisverse-site-v1', 'assets');
const MANIFEST_PATH = path.join(SOURCE_ROOT, 'manifest.json');

function fail(message) {
  throw new Error(`[asset-build] ${message}`);
}

function inside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative !== '' && !relative.startsWith('..') && !path.isAbsolute(relative);
}

function uint24LE(buffer, offset) {
  return buffer[offset] | (buffer[offset + 1] << 8) | (buffer[offset + 2] << 16);
}

function dimensionsPng(buffer) {
  const signature = Buffer.from('89504e470d0a1a0a', 'hex');
  if (buffer.length < 24 || !buffer.subarray(0, 8).equals(signature)) fail('Invalid PNG signature');
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

function dimensionsJpeg(buffer) {
  if (buffer.length < 4 || buffer[0] !== 0xff || buffer[1] !== 0xd8) fail('Invalid JPEG signature');
  const sof = new Set([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf]);
  let offset = 2;
  while (offset + 4 <= buffer.length) {
    while (offset < buffer.length && buffer[offset] !== 0xff) offset += 1;
    while (offset < buffer.length && buffer[offset] === 0xff) offset += 1;
    if (offset >= buffer.length) break;
    const marker = buffer[offset++];
    if (marker === 0xd8 || marker === 0xd9 || marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue;
    if (offset + 2 > buffer.length) break;
    const length = buffer.readUInt16BE(offset);
    if (length < 2 || offset + length > buffer.length) fail('Malformed JPEG segment');
    if (sof.has(marker)) {
      if (length < 7) fail('Malformed JPEG SOF segment');
      return { height: buffer.readUInt16BE(offset + 3), width: buffer.readUInt16BE(offset + 5) };
    }
    offset += length;
  }
  fail('JPEG dimensions not found');
}

function dimensionsWebp(buffer) {
  if (buffer.length < 30 || buffer.toString('ascii', 0, 4) !== 'RIFF' || buffer.toString('ascii', 8, 12) !== 'WEBP') {
    fail('Invalid WebP signature');
  }
  const declared = buffer.readUInt32LE(4) + 8;
  if (declared !== buffer.length) fail(`WebP RIFF length mismatch: header=${declared}, actual=${buffer.length}`);
  const chunk = buffer.toString('ascii', 12, 16);
  if (chunk === 'VP8X') {
    return { width: uint24LE(buffer, 24) + 1, height: uint24LE(buffer, 27) + 1 };
  }
  if (chunk === 'VP8L') {
    if (buffer[20] !== 0x2f) fail('Invalid lossless WebP header');
    const bits = buffer.readUInt32LE(21);
    return { width: (bits & 0x3fff) + 1, height: ((bits >> 14) & 0x3fff) + 1 };
  }
  if (chunk === 'VP8 ') {
    const start = 20;
    if (buffer.length < start + 10 || buffer[start + 3] !== 0x9d || buffer[start + 4] !== 0x01 || buffer[start + 5] !== 0x2a) {
      fail('Invalid lossy WebP frame header');
    }
    return {
      width: buffer.readUInt16LE(start + 6) & 0x3fff,
      height: buffer.readUInt16LE(start + 8) & 0x3fff
    };
  }
  fail(`Unsupported WebP chunk type: ${chunk}`);
}

function validateFormat(buffer, mimeType, output) {
  const extension = path.extname(output).toLowerCase();
  if (mimeType === 'image/webp' && extension === '.webp') return dimensionsWebp(buffer);
  if (mimeType === 'image/png' && extension === '.png') return dimensionsPng(buffer);
  if ((mimeType === 'image/jpeg' || mimeType === 'image/jpg') && (extension === '.jpg' || extension === '.jpeg')) return dimensionsJpeg(buffer);
  fail(`MIME type and extension do not match for ${output}`);
}

async function buildAsset(asset) {
  const required = ['id', 'output', 'mimeType', 'expectedBytes', 'sha256', 'width', 'height', 'parts'];
  for (const field of required) if (asset[field] === undefined) fail(`Asset is missing required field: ${field}`);
  if (!Array.isArray(asset.parts) || asset.parts.length === 0) fail(`${asset.id}: parts must be a non-empty array`);
  if (!/-v\d+\.(webp|png|jpe?g)$/i.test(asset.output)) fail(`${asset.id}: output filename must be versioned, for example name-v11.webp`);

  const outputPath = path.resolve(ROOT, asset.output);
  if (!inside(OUTPUT_ROOT, outputPath)) fail(`${asset.id}: output must be inside vectisverse-site-v1/assets`);

  const payloads = [];
  for (const part of asset.parts) {
    const partPath = path.resolve(SOURCE_ROOT, part);
    if (!inside(SOURCE_ROOT, partPath)) fail(`${asset.id}: part path escapes asset-source`);
    payloads.push((await readFile(partPath, 'utf8')).replace(/\s+/g, ''));
  }

  const base64 = payloads.join('');
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(base64) || base64.length % 4 !== 0) fail(`${asset.id}: invalid Base64 payload`);
  const buffer = Buffer.from(base64, 'base64');
  if (buffer.length !== asset.expectedBytes) fail(`${asset.id}: expected ${asset.expectedBytes} bytes, got ${buffer.length}`);

  const digest = createHash('sha256').update(buffer).digest('hex');
  if (digest.toLowerCase() !== String(asset.sha256).toLowerCase()) fail(`${asset.id}: SHA-256 mismatch`);

  const dimensions = validateFormat(buffer, asset.mimeType, asset.output);
  if (dimensions.width !== asset.width || dimensions.height !== asset.height) {
    fail(`${asset.id}: expected ${asset.width}x${asset.height}, got ${dimensions.width}x${dimensions.height}`);
  }

  await mkdir(path.dirname(outputPath), { recursive: true });
  const temporary = `${outputPath}.tmp-${process.pid}`;
  await rm(temporary, { force: true });
  await writeFile(temporary, buffer, { flag: 'wx' });
  await rename(temporary, outputPath);
  console.log(`[asset-build] Built ${asset.output} (${buffer.length} bytes, ${digest.slice(0, 12)}…)`);
}

async function main() {
  const manifest = JSON.parse(await readFile(MANIFEST_PATH, 'utf8'));
  if (manifest.version !== 1 || !Array.isArray(manifest.assets)) fail('manifest.json must contain version 1 and an assets array');
  if (manifest.assets.length === 0) {
    console.log('[asset-build] No reconstructed assets listed; existing website assets are unchanged.');
    return;
  }
  const outputs = new Set();
  for (const asset of manifest.assets) {
    if (outputs.has(asset.output)) fail(`Duplicate output in manifest: ${asset.output}`);
    outputs.add(asset.output);
    await buildAsset(asset);
  }
  console.log(`[asset-build] Successfully validated ${manifest.assets.length} asset(s).`);
}

main().catch((error) => {
  console.error(error.message || error);
  process.exitCode = 1;
});
