class OpenConnect {
    constructor(wallet, connect_data, btn_connect, menu_container) {
        this.wallet = wallet;
        this.connect_data = connect_data;
        this.btn_connect = btn_connect;
        this.menu_container = menu_container;
        this.copyaddress_btn = null;
        this.leaveconnect_btn = null;
        this.address = null;
        this.menuOpen = false;
        this.is_connected = false;
    }

    openWallet() {
        const { wallet, connect_data } = this;
        const walletUrlWithParams = connect_data && connect_data.appUrl ? `${wallet}?appUrlConnect=${connect_data.appUrl}` : wallet;
        window.open(walletUrlWithParams, '_blank');
    }

    getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            const [cookieName, cookieValue] = cookie.split('=');
            if (cookieName === name) {
                return cookieValue;
            }
        }
        return null;
    }

    isConnectedWallet() {
        this.is_connected =  this.getCookie("OpenConnection") !== null
        return this.is_connected;
    }

    updateConnectBtn() {
        const connect_btn = document.getElementById(this.btn_connect);

        if (connect_btn) {
            const is_connected = this.isConnectedWallet();

            const commonBtnStyles = {
                position: "absolute",
                width: "170px",
                height: "45px",
                left: "86%",
                borderRadius: "20px",
                background: "rgb(42, 41, 41)",
                border: "none",
                color: "white",
                fontFamily: "Dela Gothic One",
                paddingLeft: "30px",
                cursor: "pointer",
                transition: ".5s",
            };

            Object.assign(connect_btn.style, commonBtnStyles);

            if (is_connected) {
                const address = this.getAddress();
                this.address = address;
                const truncateAddress = this.truncateAddress(address);
                connect_btn.innerText = truncateAddress;
            } else {
                connect_btn.innerText = "OpenConnect";
            }

            const openCoinImg = this.createImage("imgCoin_OpenConnect", "https://ton.app/media/jetton-1dee163e-3a1e-4b0f-a803-d74636655010.jpg", {
                position: "absolute",
                borderRadius: "40px",
                width: "28px",
                height: "28px",
                left: "3%",
                top: "20%",
            });
            connect_btn.appendChild(openCoinImg);

            if (!this.copyaddress_btn) {
                this.copyaddress_btn = this.createButton("copyaddress_OpenConnect", "Copy Address", "-300%", "20%", true);
            }
            if (!this.leaveconnect_btn) {
                this.leaveconnect_btn = this.createButton("leaveconnect_OpenConnect", "Disconnect", "-300%", "90%", false, true);
                this.leaveconnect_btn.href = `connection/${this.getCookie('OpenConnection')}/delete`;
            }

            this.updateEventListener();
            this.applyHoverEffect(connect_btn);
        }
    }

    createButton(id, text, top, left, isCopyAddress = false, isLeaveConnect = false) {
        const button = document.createElement("a");
        button.id = id;
        button.innerText = text;
        button.style.cssText = `
            position: absolute;
            width: 140px;
            height: 45px;
            top: ${top};
            left: 0;
            border-radius: ${isCopyAddress ? '0px' : '0px 0px 20px 20px'};
            background: rgb(42, 41, 41);
            border: none;
            color: ${isCopyAddress || isLeaveConnect ? 'rgb(150, 150, 150)' : 'white'};
            font-family: Dela Gothic One;
            padding-left: 30px;
            cursor: pointer;
            transition: .5s;
            font-size: 11px;
            padding-top: 10px;
            text-decoration: none;
        `;
        document.getElementById(this.btn_connect).appendChild(button);
        return button;
    }

    createImage(id, src, styles) {
        const img = document.createElement("img");
        img.id = id;
        img.src = src;
        Object.assign(img.style, styles);
        return img;
    }

    updateEventListener() {
        const btn = document.getElementById(this.btn_connect);
        const copyaddress_btn = this.copyaddress_btn;
        const leaveconnect_btn = this.leaveconnect_btn;

        btn.addEventListener("click", () => this.onButtonClick());

        [copyaddress_btn, leaveconnect_btn].forEach(button => {
            button.addEventListener("mouseover", () => button.style.color = "white");
            button.addEventListener("mouseout", () => button.style.color = "rgb(150, 150, 150)");
        });

        copyaddress_btn.addEventListener("click", () => {
            const address = this.getCookie("OpenAddress");
            navigator.clipboard.writeText(address);
        });
    }

    applyHoverEffect(element) {
        element.addEventListener("mouseover", () => element.style.transform = "scale(1.1)");
        element.addEventListener("mouseout", () => element.style.transform = "scale(1)");
    }

    onButtonClick() {
        if (this.menuOpen) {
            this.closeConnectMenu();
        } else if (this.is_connected) {
            this.showConnectMenu();
        } else {
            this.openWallet();
        }
    }

    showConnectMenu() {
        const connect_btn = document.getElementById(this.btn_connect);
        if (connect_btn) {
            connect_btn.style.borderRadius = "20px 20px 0px 0px";
            this.copyaddress_btn.style.top = "90%";
            this.leaveconnect_btn.style.top = "190%";
            this.menuOpen = true;
        }
    }

    closeConnectMenu()
    {
        const connect_btn = document.getElementById(this.btn_connect);
        if (connect_btn) {
            connect_btn.style.borderRadius = "20px 20px 20px 20px";
            this.copyaddress_btn.style.top = "-300%";
            this.leaveconnect_btn.style.top = "-300%";
            this.menuOpen = false;
        }
    }

    updateStyleLinks() {
        const linkElement = document.createElement("link");
        linkElement.href = "https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Lilita+One&family=Merriweather+Sans:wght@300&family=Odor+Mean+Chey&family=Rammetto+One&family=Roboto:wght@100&family=Rubik:wght@300&display=swap";
        linkElement.rel = "stylesheet";
        document.head.appendChild(linkElement);
    }

    truncateAddress(address) {
        const lengthToShow = 5;
        return `${address.substring(0, lengthToShow)}...${address.substring(address.length - lengthToShow)}`;
    }

    getAddress() {
        return this.getCookie("OpenAddress");
    }
}