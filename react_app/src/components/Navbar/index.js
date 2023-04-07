import React from "react";
import { Nav, NavLink, NavMenu }
	from "./NavbarElements";

const Navbar = () => {
return (
	<>
	<Nav>
		<NavMenu>
		<NavLink to="/packages" activeStyle>
			Packages
		</NavLink>
		<NavLink to="/upload" activeStyle>
			Upload
		</NavLink>
		<NavLink to="/rating" activeStyle>
			Rating
		</NavLink>
		<NavLink to="/login" activeStyle>
			Log In Here
		</NavLink>
		</NavMenu>
	</Nav>
	</>
);
};

export default Navbar;
