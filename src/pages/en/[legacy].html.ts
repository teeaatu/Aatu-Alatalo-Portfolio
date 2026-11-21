import { legacyPaths, legacyRedirect } from '../../utils/legacy-redirects';

export const getStaticPaths = () => legacyPaths('en');
export const GET = legacyRedirect;
