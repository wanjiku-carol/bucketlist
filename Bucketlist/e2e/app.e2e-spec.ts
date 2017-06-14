import { BucketlistPage } from './app.po';

describe('bucketlist App', () => {
  let page: BucketlistPage;

  beforeEach(() => {
    page = new BucketlistPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
