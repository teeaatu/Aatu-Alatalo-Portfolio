import { legacyPaths, legacyRedirect } from '../utils/legacy-redirects';

export const getStaticPaths = () => legacyPaths('fi');
export const GET = legacyRedirect;
