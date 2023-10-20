
class IPRGas:


class IPROil:

    def __init__(self, k, re, rw, s, res_pres, oil_fvf, n_points, bhp, viscosity):
        self.k = k
        self.re = re
        self.rw = rw
        self.s = s
        self.res_pres = res_pres
        self.oil_fvf = oil_fvf
        self.n_points = n_points
        self.bhp = bhp
        self.viscosity = viscosity

    def Fetkovich(self):
        """
            Calculate the oil production rate using the Fetkovich IPR model.

            The Fetkovich equation is represented as:
            Qo = C * (Pr^(-2) - Pwf^(-2))^n

            Where:
            Qo: Oil production rate
            C : Constant that depends on permeability, formation thickness, oil formation volume factor, viscosity, and skin factor.
            Pr: Reservoir pressure
            Pwf: Wellbore flowing pressure
            n : Exponent, often equated to the number of data points used in curve fitting the IPR data

            Returns:
            float: Calculated oil production rate (Qo)
        """

        h = 1  # Please replace with the correct thickness value

        C = (2 * 3.141592653589793 * self.k * h) / (self.oil_fvf * self.viscosity * self.s)

        # Now, compute Qo using Fetkovich equation
        Pr_inv_square = (1 / self.res_pres) ** 2
        Pwf_inv_square = (1 / self.bhp) ** 2

        n = self.n_points  # Using n_points as 'n' for the formula

        Qo = C * (Pr_inv_square - Pwf_inv_square) ** n

        return Qo




    def Darcy_IPR(self):
        """Function to calculate IPR using Darcy's Equation.  It returns a list with a pair of Pressure and rates"""
        PwfList = []
        QList = []
        QList.append(0)
        PwfList.append(self.res_pres)

        mStep = P / nPoints
        i = 1

        while (i <= nPoints):
            Pwf = PwfList[i - 1] - mStep
            Q = (k * h / visc) * (P - Pwf) / (141.2 * OilFVF * visc * (math.log(re / rw) - 0.75 + s))

            QList.append(Q)
            PwfList.append(Pwf)

            i = i + 1

        DarcyList = [QList, PwfList]

        return DarcyList

    def VogelIPR(P, Pb, Pwf, Qo, nPoints):
        """Function to calculate IPR using Vogel's Equation.  It returns a list with a pair of Pressure and rates"""

        PwfList = []
        QList = []
        QList.append(0)
        PwfList.append(P)
        VogelList = []
        mStep = P / nPoints
        i = 1

        if Pwf >= Pb:
            J = Qo / (P - Pwf)

        else:
            J = Qo / ((P - Pb) + ((Pb / 1.8) * (1 - 0.2 * (Pwf / Pb) - 0.8 * (Pwf / Pb) ** 2)))

        while (i <= nPoints):

            Pwfs = PwfList[i - 1] - mStep

            if Pwfs >= Pb:

                Q = J * (P - Pwfs)
            else:

                Qb = J * (P - Pb)
                Q = Qb + (J * Pb / 1.8) * (1 - 0.2 * (Pwfs / Pb) - 0.8 * (Pwfs / Pb) ** 2)

            QList.append(Q)
            PwfList.append(Pwfs)

            i = i + 1

        VogelList = [QList, PwfList]

        return VogelList

    def Vogel_DarcyIPR(P, k, h, visc, re, rw, s, OilFVF, Temp, Pb, nPoints):
        """Function to calculate IPR using Vogel's Equation.  It returns a list with a pair of Pressure and rates"""

        PwfList = []
        QList = []
        QList.append(0)
        PwfList.append(P)
        VogelList = []
        mStep = P / nPoints
        i = 1

        J = (k * h / visc) / (141.2 * OilFVF * visc * (math.log(re / rw) - 0.75 + s))

        while (i <= nPoints):

            Pwfs = PwfList[i - 1] - mStep

            if Pwfs >= Pb:
                Q = J * (P - Pwfs)

            else:

                Qb = J * (P - Pb)
                Q = Qb + (J * Pb / 1.8) * (1 - 0.2 * (Pwfs / Pb) - 0.8 * (Pwfs / Pb) ** 2)

            QList.append(Q)
            PwfList.append(Pwfs)

            i = i + 1

        VogelList = [QList, PwfList]
        return VogelList

