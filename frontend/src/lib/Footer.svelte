<script>
    import {Footer, FooterBrand, FooterCopyright, FooterIcon, FooterLink, FooterLinkGroup} from 'flowbite-svelte';
    import {GithubSolid, LinkedinSolid} from 'flowbite-svelte-icons';
</script>


<Footer class="border-t-2 dark:border-gray-700" footerType="socialmedia">
    <div class="mt-5 mb-5"></div>
    <div class="md:flex md:justify-between mt-5">
        <div class="mb-4 md:mb-0">
            <FooterBrand alt="Django Logo" href="/" name="Django Rest Trello" src="/django-icon-svgrepo-com%20(1).svg"/>
        </div>
        <div class="grid grid-cols-2 gap-8 sm:gap-6 sm:grid-cols-3">
            <div>
                <h2 class="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Resources</h2>
                <FooterLinkGroup>
                    <FooterLink href="https://flowbite-svelte.com/" liClass="mb-4">Flowbite Svelte</FooterLink>
                    <FooterLink href="https://tailwindcss.com/" liClass="mb-4">Tailwind CSS</FooterLink>
                </FooterLinkGroup>
            </div>
            <div>
                <h2 class="mb-6 text-sm font-semibold uppercase text-gray-900 dark:text-white">Follow Me</h2>
                <FooterLinkGroup>
                    <FooterLink href="https://github.com/farzan-alaei" liClass="mb-4">GitHub</FooterLink>
                    <FooterLink href="https://www.linkedin.com/in/farzanalaei" liClass="mb-4">LinkedIn</FooterLink>
                </FooterLinkGroup>
            </div>
            <div>
                <h2 class="mb-6 text-sm font-semibold uppercase text-gray-900 dark:text-white">Legal</h2>
                <FooterLinkGroup>
                    <FooterLink href="/" liClass="mb-4">Privacy Policy</FooterLink>
                    <FooterLink href="/" liClass="mb-4">Terms & Conditions</FooterLink>
                </FooterLinkGroup>
            </div>
        </div>
    </div>
    <hr class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8"/>
    <div class="sm:flex sm:items-center sm:justify-between">
        <FooterCopyright by="Django Rest Trello™" href="/"/>
        <div class="flex mt-4 space-x-6 rtl:space-x-reverse sm:justify-center sm:mt-0">
            <FooterIcon href="https://www.linkedin.com/in/farzanalaei">
                <LinkedinSolid
                        class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white"/>
            </FooterIcon>
            <FooterIcon href="https://github.com/farzan-alaei">
                <GithubSolid
                        class="w-5 h-5 text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white"/>
            </FooterIcon>
        </div>
    </div>
</Footer>